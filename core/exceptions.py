class WorkerCompensationError(Exception):
    """工伤助手基础异常"""
    pass

class DatabaseError(WorkerCompensationError):
    """数据库操作异常"""
    pass

class TemplateError(WorkerCompensationError):
    """模板处理异常"""
    pass