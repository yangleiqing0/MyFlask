from db_create import db
from datetime import datetime
from .basemodel import BaseModel, Base
from .user import User
from .variables import Variables
from .case_group import CaseGroup
from .request_headers import RequestHeaders
from .mail import Mail
from .testcase_scene import TestCaseScene
from .testcase import TestCases
from .testcase_start_times import TestCaseStartTimes
from .testcase_scene_result import TestCaseSceneResult
from .database import Mysql
from .time_message import TimeMessage
from .testcase_result import TestCaseResult
from .job import Job
from .test import TestGroup


models_list = []
[models_list.append(eval(_model)) for _model in dir() if "__" not in _model
 and _model[0].isupper() and _model not in ["BaseModel", "Base"]]

