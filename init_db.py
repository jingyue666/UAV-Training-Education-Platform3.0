import sqlite3
import os

os.makedirs("data", exist_ok=True)
DB_PATH = os.path.join("data", "drone_platform.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS videos;
DROP TABLE IF EXISTS exam_records;
DROP TABLE IF EXISTS exam_wrong_questions;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    real_name TEXT,
    phone TEXT,
    role TEXT,
    level TEXT,
    status TEXT DEFAULT '正常'
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    level TEXT,
    category TEXT,
    price REAL,
    duration INTEGER
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    category TEXT,
    level TEXT,
    url TEXT,
    cover TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exam_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    exam_type TEXT,
    score REAL,
    total_score REAL,
    pass_status TEXT,
    submitted_at TIMESTAMP
);

CREATE TABLE exam_wrong_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_record_id INTEGER,
    question TEXT,
    user_answer TEXT,
    correct_answer TEXT,
    explanation TEXT
);

INSERT INTO users (username, password, real_name, phone, role, level, status)
VALUES ('admin','admin123','管理员','','管理员','高级','正常');

INSERT INTO users (username, password, real_name, phone, role, level, status)
VALUES ('student','123456','张三','13811111111','学员','初级','正常');
""")

demo_videos = [
    ("无人机系统原理入门", "讲解无人机组成、飞行原理、机架与电机基础", "基础理论模块", "初级", "https://www.w3school.com.cn/i/movie.mp4", ""),
    ("航空法律法规与空域规范", "民用无人机飞行法规、禁飞区、报备流程详解", "基础理论模块", "中级", "https://www.w3school.com.cn/i/movie.mp4", ""),
    ("无人机基础起降实操教学", "零基础练习起飞、悬停、定点降落技巧", "实操技能模块", "初级", "https://www.w3school.com.cn/i/movie.mp4", ""),
    ("重庆山地地形飞行适配训练", "山地风场判断、绕障飞行、地形自适应操作", "实操技能模块", "高级", "https://www.w3school.com.cn/i/movie.mp4", ""),
    ("农业植保无人机作业流程", "农田测绘、药剂喷洒、航线规划全流程", "行业应用模块", "中级", "https://www.w3school.com.cn/i/movie.mp4", ""),
    ("城市治理巡检应用实战", "市容巡检、违章排查、河道巡查案例教学", "行业应用模块", "高级", "https://www.w3school.com.cn/i/movie.mp4", ""),
    ("无人机项目接单与报价技巧", "市场获客、项目报价、合同基础规范", "商业运营模块", "中级", "https://www.w3school.com.cn/i/movie.mp4", ""),
    ("航拍文旅项目商业策划", "文旅拍摄方案、团队搭建、品牌推广思路", "商业运营模块", "高级", "https://www.w3school.com.cn/i/movie.mp4", "")
]

for v in demo_videos:
    c.execute("INSERT INTO videos (title, description, category, level, url, cover) VALUES (?,?,?,?,?,?)", v)

conn.commit()
conn.close()
print("✅ 数据库初始化完成")
