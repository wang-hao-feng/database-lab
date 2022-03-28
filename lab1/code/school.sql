CREATE DATABASE IF NOT EXISTS school
    DEFAULT CHARACTER SET = 'utf8mb4' COLLATE utf8mb4_bin;

USE school;

#创建实体
CREATE Table IF NOT EXISTS 课程
(
    课程号 VARCHAR(10) NOT NULL,
    课程名 VARCHAR(20) NOT NULL,
    PRIMARY KEY(课程号)
);

CREATE Table IF NOT EXISTS 学生
(
    学号 VARCHAR(20) NOT NULL,
    姓名 VARCHAR(10) NOT NULL,
    年龄 INT CHECK(0 <= 年龄 AND 年龄 <= 150) DEFAULT NULL,
    性别 VARCHAR(2) CHECK(性别 = '男' OR 性别 = '女') DEFAULT NULL,
    年级 VARCHAR(5) CHECK(年级 = '大一' OR 年级 = '大二' OR 
                                年级 = '大三' OR 年级 = '大四') DEFAULT NULL,
    PRIMARY KEY(学号)
);

CREATE Table IF NOT EXISTS 教师
(
    工号 VARCHAR(20) NOT NULL,
    姓名 VARCHAR(10) NOT NULL,
    工资 INT DEFAULT NULL,
    PRIMARY KEY(工号)
);

CREATE Table IF NOT EXISTS 院系
(
    院系代码 VARCHAR(20) NOT NULL,
    院系名 VARCHAR(10) NOT NULL,
    PRIMARY KEY(院系代码)
);

CREATE Table IF NOT EXISTS 教室
(
    楼号 VARCHAR(10) NOT NULL,
    房间号 VARCHAR(20) NOT NULL,
    容量 INT DEFAULT NULL,
    PRIMARY KEY(楼号, 房间号)
);

CREATE Table IF NOT EXISTS 研讨室
(
    楼号 VARCHAR(10) NOT NULL,
    房间号 VARCHAR(20) NOT NULL,
    PRIMARY KEY(楼号, 房间号)
);

CREATE Table IF NOT EXISTS 社团
(
    社团代码 VARCHAR(20) NOT NULL,
    社团名 VARCHAR(30),
    PRIMARY KEY(社团代码)
);

CREATE Table IF NOT EXISTS 宿舍
(
    楼号 VARCHAR(10) NOT NULL,
    床号 VARCHAR(20) NOT NULL,
    PRIMARY KEY(楼号, 床号)
);

#创建联系
CREATE TABLE IF NOT EXISTS 选修
(
    学号 VARCHAR(20) NOT NULL,
    课程号 VARCHAR(10) NOT NULL,
    成绩 INT CHECK(0 <= 成绩 AND 成绩 <= 100) DEFAULT NULL,
    PRIMARY KEY(学号, 课程号),
    FOREIGN KEY(学号) REFERENCES 学生(学号),
    FOREIGN KEY(课程号) REFERENCES 课程(课程号)
);

CREATE Table IF NOT EXISTS 任课
(
    工号 VARCHAR(20) NOT NULL,
    课程号 VARCHAR(10) NOT NULL,
    PRIMARY KEY(工号, 课程号),
    FOREIGN KEY(工号) REFERENCES 教师(工号),
    FOREIGN KEY(课程号) REFERENCES 课程(课程号)
);

CREATE Table IF NOT EXISTS 开设
(
    院系代码 VARCHAR(20) NOT NULL,
    课程号 VARCHAR(10) NOT NULL,
    PRIMARY KEY(院系代码, 课程号),
    FOREIGN KEY(院系代码) REFERENCES 院系(院系代码),
    FOREIGN KEY(课程号) REFERENCES 课程(课程号)
);

CREATE Table IF NOT EXISTS 位于
(
    课程号 VARCHAR(10) NOT NULL,
    楼号 VARCHAR(10) NOT NULL,
    房间号 VARCHAR(20) NOT NULL,
    PRIMARY KEY(课程号, 楼号, 房间号),
    FOREIGN KEY(课程号) REFERENCES 课程(课程号),
    FOREIGN KEY(楼号, 房间号) REFERENCES 教室(楼号, 房间号)
);

CREATE Table IF NOT EXISTS 属于
(
    学号 VARCHAR(20) NOT NULL,
    院系代码 VARCHAR(20) NOT NULL,
    PRIMARY KEY(学号, 院系代码),
    FOREIGN KEY(学号) REFERENCES 学生(学号),
    FOREIGN KEY(院系代码) REFERENCES 院系(院系代码)
);

CREATE Table IF NOT EXISTS 借用
(
    学号 VARCHAR(20) NOT NULL,
    楼号 VARCHAR(10) NOT NULL,
    房间号 VARCHAR(20) NOT NULL,
    开始时间 DATETIME NOT NULL,
    结束时间 DATETIME NOT NULL,
    PRIMARY KEY(学号, 楼号, 房间号),
    FOREIGN KEY(学号) REFERENCES 学生(学号),
    FOREIGN KEY(楼号, 房间号) REFERENCES 研讨室(楼号, 房间号)
);

CREATE Table IF NOT EXISTS 参加
(
    学号 VARCHAR(20) NOT NULL,
    社团代码 VARCHAR(20) NOT NULL,
    PRIMARY KEY(学号, 社团代码),
    FOREIGN KEY(学号) REFERENCES 学生(学号),
    FOREIGN KEY(社团代码) REFERENCES 社团(社团代码)
);

CREATE Table IF NOT EXISTS 住宿
(
    学号 VARCHAR(20) NOT NULL,
    楼号 VARCHAR(10) NOT NULL,
    床号 VARCHAR(20) NOT NULL,
    PRIMARY KEY(学号, 楼号, 床号),
    FOREIGN KEY(学号) REFERENCES 学生(学号),
    FOREIGN KEY(楼号, 床号) REFERENCES 宿舍(楼号, 床号)
);

CREATE Table IF NOT EXISTS 指导
(
    工号 VARCHAR(20) NOT NULL,
    社团代码 VARCHAR(20) NOT NULL,
    PRIMARY KEY(工号, 社团代码),
    FOREIGN KEY(工号) REFERENCES 教师(工号),
    FOREIGN KEY(社团代码) REFERENCES 社团(社团代码)
);

CREATE Table IF NOT EXISTS 任职
(
    工号 VARCHAR(20) NOT NULL,
    院系代码 VARCHAR(20) NOT NULL,
    PRIMARY KEY(工号, 院系代码),
    FOREIGN KEY(工号) REFERENCES 教师(工号),
    FOREIGN KEY(院系代码) REFERENCES 院系(院系代码)
);

CREATE VIEW 住宿学生信息(学号, 姓名, 年龄, 性别, 年级, 专业, 宿舍楼号, 宿舍床号) AS
SELECT 学号, 姓名, 年龄, 性别, 年级, 院系名, 楼号, 床号
FROM 学生 NATURAL JOIN 属于 NATURAL JOIN 院系 NATURAL JOIN 住宿 NATURAL JOIN 宿舍;

CREATE VIEW 课程信息(课程号, 课程名, 任课老师, 开课院系, 教室楼号, 教室房间号) AS
SELECT 课程号, 课程名, 姓名, 院系名, 楼号, 房间号
FROM 课程 NATURAL JOIN 任课 NATURAL JOIN 教师 NATURAL JOIN 开设 NATURAL JOIN 院系 
        NATURAL JOIN 位于 NATURAL JOIN 教室;

ALTER Table 借用 ADD INDEX (开始时间, 结束时间);

#插入实体
INSERT INTO 课程 VALUES
("CS001", "大计基"),
("CS002", "高级语言程序设计"),
("MA001", "微积分"),
("MA002", "线性代数"),
("AS001", "航天技术概论"),
("AS002", "航天器结构");

INSERT INTO 学生 VALUES
("001", "李天斯", 18, "男", "大一"),
("002", "王里", 19, "男", "大一"),
("003", "张蔷", 20, "女", "大三"),
("004", "李华", 20, "男", "大三"),
("005", "孙七", 19, "男", "大二"),
("006", "张红", 18, "女", "大二");

INSERT INTO 教师 VALUES
("001", "张三", 5000),
("002", "李四", 5000),
("003", "王五", 5000),
("004", "赵六", 5000);

INSERT INTO 院系 VALUES
("CS", "计算机"),
("MA", "数学"),
("AS", "航天");

INSERT INTO 教室 VALUES
("01", "101", 50),
("01", "102", 50),
("01", "103", 50),
("01", "104", 50);

INSERT INTO 研讨室 VALUES
("01", "001"),
("01", "002");

INSERT INTO 社团 VALUES
("001", "足球社"),
("002", "羽毛球社");

INSERT INTO 宿舍 VALUES
("01", "001"),
("01", "002"),
("01", "003"),
("01", "004"),
("02", "001"),
("02", "002");

#插入关系
INSERT INTO 选修 VALUES
("001", "CS001", 90),
("001", "CS002", 90),
("002", "CS001", 90),
("002", "CS002", 90);

INSERT INTO 任课 VALUES
("001", "CS001"),
("001", "CS002"),
("002", "CS001"),
("002", "CS002"),
("003", "MA001"),
("003", "MA002"),
("004", "AS001"),
("004", "AS002");

INSERT INTO 开设 VALUES
("CS", "CS001"),
("CS", "CS002"),
("MA", "MA001"),
("MA", "MA002"),
("AS", "AS001"),
("AS", "AS002");

INSERT INTO 位于 VALUES
("CS001", "01", "101"),
("CS002", "01", "101"),
("MA001", "01", "102"),
("MA002", "01", "102"),
("AS001", "01", "103"),
("AS002", "01", "103");

INSERT INTO 属于 VALUES
("001", "CS"),
("002", "CS"),
("003", "MA"),
("004", "MA"),
("005", "AS"),
("006", "AS");

INSERT INTO 借用 VALUES
("004", "01", "001", "2021-12-1 18:30:00", "2021-12-1 20:00:00");

INSERT INTO 参加 VALUES
("001", "001"),
("002", "001"),
("004", "002"),
("006", "002");

INSERT INTO 住宿 VALUES
("001", "01", "001"),
("002", "01", "002"),
("003", "02", "001"),
("006", "02", "002");

INSERT INTO 指导 VALUES
("002", "001"),
("002", "002");

INSERT INTO 任职 VALUES
("001", "CS"),
("002", "CS"),
("003", "MA"),
("004", "AS");