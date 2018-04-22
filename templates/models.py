from datetime import datetime
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)  # weiyixing
    info = db.Column(db.TEXT)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DATETIME, unique=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)
    userlogs = db.relationship("userlog", backref="user")
    moviecols = db.relationship("Moviecol", backref="user")
    comment = db.relationship("Comment", backref="user")

    def __repr__(self):
        return "<user %r>" % self.name
# 会员登陆日志


class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 外键关联
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<userlogin %r>" % self.userlog

# 标签


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    movie = db.relationship("Movie", backref="tag")

    def __repr__(self):
        return "<tag %r>" % self.name


class Movie (db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    area = db.Column(db.String(255), unique=True)  # 上映地区
    relase_time = db.Column(db.Date)
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    star = db.Column(db.SmallInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    lenth = db.Column(db.String(100))
    moviecols = db.relationship("Moviecol", backref="movie")
    comment = db.relationship("Comment", backref="movie")

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)

    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return"<Preview %s>" % self.title


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<comment %r>" % self.id


# movieclo 收藏
class moviecol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Moviecol %r>" % self.id

# 权限及角色数据模型设计


class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Auth %r>" % self.name
# 权限


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    admins = db.relationship("Admin", backref="role")

    def __repr__(self):
        return "<role %r>" % self.name

# 管理员、登陆日志、操作日志数据模型设计


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 管理员的相关信息
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100), unique=True)
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship("Adminlog", backref="admin")
    oplogs = db.relationship("Oplog", backref="admin")

    def __repr__(self):
        return "<admin %r>" % self.name

# 管理员登陆日志


class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 管理员的相关信息
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<adminlog %r>" % self.name
# 操作日志


class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 管理员的相关信息
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 所属管理员
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    reason = db.Column(db.String(600))

    def __repr__(self):
        return "<op %r>" % self.name


if __name__ == "__main__":
    """
        from werkzeug.security import generate_password_hash #生成密码
    admin = Admin(
        name = "admin1",
        pwd = generate_password_hash("admin1"),
        is_super= 0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
    
    
    """

    db.create_all()
