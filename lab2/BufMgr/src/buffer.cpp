/**
 * @author See Contributors.txt for code contributors and overview of BadgerDB.
 *
 * @section LICENSE
 * Copyright (c) 2012 Database Group, Computer Sciences Department, University of Wisconsin-Madison.
 */

#include <memory>
#include <iostream>
#include "buffer.h"
#include "exceptions/buffer_exceeded_exception.h"
#include "exceptions/page_not_pinned_exception.h"
#include "exceptions/page_pinned_exception.h"
#include "exceptions/bad_buffer_exception.h"
#include "exceptions/hash_not_found_exception.h"

namespace badgerdb { 

BufMgr::BufMgr(std::uint32_t bufs)
	: numBufs(bufs) {
	bufDescTable = new BufDesc[bufs];

  for (FrameId i = 0; i < bufs; i++) 
  {
  	bufDescTable[i].frameNo = i;
  	bufDescTable[i].valid = false;
  }

  bufPool = new Page[bufs];

	int htsize = ((((int) (bufs * 1.2))*2)/2)+1;
  hashTable = new BufHashTbl (htsize);  // allocate the buffer hash table

  clockHand = bufs - 1;
}


BufMgr::~BufMgr() 
{
	//写回脏页面
	for(FrameId i = 0; i < this->numBufs; i++)
	{
		if(!this->bufDescTable[i].valid)
			continue;
		PageId frame = this->bufDescTable[i].frameNo;
		if(this->bufDescTable[i].dirty)
			this->bufDescTable[i].file->writePage(this->bufPool[frame]);
	}
	//释放缓冲池
	delete[] this->bufPool;
	//释放BufDec
	delete[] this->bufDescTable;
	//释放哈希表
	delete this->hashTable;
}

void BufMgr::advanceClock()
{
	this->clockHand++;
	this->clockHand %= this->numBufs;
}

void BufMgr::allocBuf(FrameId & frame) 
{
	FrameId pin_page_num = 0;
	while(1)
	{
		//所有页面是否都被固定
		if(pin_page_num >= this->numBufs)
			throw BufferExceededException();
		//更新表针
		this->advanceClock();
		//页面是否有效
		if(!this->bufDescTable[this->clockHand].valid)
			break;
		//页面最近是否被访问
		if(this->bufDescTable[this->clockHand].refbit)
		{
			this->bufDescTable[this->clockHand].refbit = false;
			continue;
		}
		//页面是否被固定
		if(this->bufDescTable[this->clockHand].pinCnt > 0)
		{
			pin_page_num++;
			continue;
		}
		break;
	}
	//是否是脏页面
	if(this->bufDescTable[this->clockHand].dirty)
		this->bufDescTable[this->clockHand].file->writePage(this->bufPool[this->bufDescTable[this->clockHand].frameNo]);
	//有效页面从哈希表中删除
	if(this->bufDescTable[this->clockHand].valid)
	{
		this->hashTable->remove(this->bufDescTable[this->clockHand].file, this->bufDescTable[this->clockHand].pageNo);
		this->bufDescTable[this->clockHand].Clear();
	}
	frame = this->clockHand;
}
	
void BufMgr::readPage(File* file, const PageId pageNo, Page*& page)
{
	FrameId frameNo;
	try
	{
		this->hashTable->lookup(file, pageNo, frameNo);
		this->bufDescTable[frameNo].refbit = true;
		this->bufDescTable[frameNo].pinCnt++;
	}
	catch(HashNotFoundException e)
	{
		this->allocBuf(frameNo);
		this->bufPool[frameNo] = file->readPage(pageNo);
		this->hashTable->insert(file, pageNo, frameNo);
		this->bufDescTable[frameNo].Set(file, pageNo);
	}
	page = &this->bufPool[frameNo];
}

void BufMgr::unPinPage(File* file, const PageId pageNo, const bool dirty) 
{
	FrameId frameNo;
	//查找当前页是否在哈希表中
	try
	{
		this->hashTable->lookup(file, pageNo, frameNo);
	}
	catch(HashNotFoundException e)
	{
		return;
	}

	//pinCnt值为0
	if(this->bufDescTable[frameNo].pinCnt == 0)
		throw PageNotPinnedException(file->filename(), pageNo, frameNo);
	
	//pinCnt值不为0
	if(dirty)
		this->bufDescTable[frameNo].dirty = true;
	this->bufDescTable[frameNo].pinCnt--;
}

void BufMgr::flushFile(const File* file) 
{
	for(FrameId i = 0; i < this->numBufs; i++)
	{
		if(this->bufDescTable[i].file != file)
			continue;
		if(!this->bufDescTable[i].valid)
			throw BadBufferException(i, this->bufDescTable[i].dirty, this->bufDescTable[i].valid, this->bufDescTable[i].refbit);
		if(this->bufDescTable[i].pinCnt > 0)
			throw PagePinnedException(file->filename(), this->bufDescTable[i].pageNo, this->bufDescTable[i].frameNo);
		if(this->bufDescTable[i].dirty)
		{
			this->bufDescTable[i].file->writePage(this->bufPool[i]);
			this->bufDescTable[i].dirty = false;
		}
		this->hashTable->remove(this->bufDescTable[i].file, this->bufDescTable[i].pageNo);
		this->bufDescTable[i].Clear();
	}
}

void BufMgr::allocPage(File* file, PageId &pageNo, Page*& page) 
{
	FrameId frameNo;
	this->allocBuf(frameNo);
	this->bufPool[frameNo] = file->allocatePage();
	
	page = &this->bufPool[frameNo];
	pageNo = page->page_number();

	this->hashTable->insert(file, pageNo, frameNo);
	this->bufDescTable[frameNo].Set(file, pageNo);
}

void BufMgr::disposePage(File* file, const PageId PageNo)
{
	FrameId frameNo;
	//如果在缓冲池中，则删除
    try
	{
		this->hashTable->lookup(file, PageNo, frameNo);
		this->hashTable->remove(this->bufDescTable[frameNo].file, this->bufDescTable[frameNo].pageNo);
		this->bufDescTable[frameNo].Clear();
	}
	catch(HashNotFoundException e)
	{}
	file->deletePage(PageNo);
}

void BufMgr::printSelf(void) 
{
  BufDesc* tmpbuf;
	int validFrames = 0;
  
  for (std::uint32_t i = 0; i < numBufs; i++)
	{
  	tmpbuf = &(bufDescTable[i]);
		std::cout << "FrameNo:" << i << " ";
		tmpbuf->Print();

  	if (tmpbuf->valid == true)
    	validFrames++;
  }

	std::cout << "Total Number of Valid Frames:" << validFrames << "\n";
}

}
