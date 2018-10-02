#coding=utf-8
from tensorflow_serving.apis import model_service_pb2
from tensorflow_serving.apis import model_service_pb2_grpc
from tensorflow_serving.apis import model_management_pb2
from tensorflow_serving.config import model_server_config_pb2
from tensorflow_serving.util import status_pb2
from google.protobuf import text_format
import grpc
import sys

"""
scripts function test for grpc reload
"""
def run_reload_one_config():
  """
  测试gRPC的reloadconfig接口
  :return:
  """
  channel = grpc.insecure_channel('yourip:port')
  stub = model_service_pb2_grpc.ModelServiceStub(channel)
  request = model_management_pb2.ReloadConfigRequest()  ##message ReloadConfigRequest
  model_server_config = model_server_config_pb2.ModelServerConfig()

  config_list = model_server_config_pb2.ModelConfigList()##message ModelConfigList
  ####try to add one config
  one_config = config_list.config.add() #
  one_config.name= "test1"
  one_config.base_path = "/home/model/model1"
  one_config.model_platform="tensorflow"

  model_server_config.model_config_list.CopyFrom(config_list) #one of

  request.config.CopyFrom(model_server_config)

  print(request.IsInitialized())
  print(request.ListFields())

  responese = stub.HandleReloadConfigRequest(request,10)
  if responese.status.error_code ==0:
      print("reload sucessfully")
  else:
      print("reload error!")
      print(responese.status.error_code)
      print(responese.status.error_message)

def parse_config_file():
    """
    测试读取config_file并回写
    :return:
    """
    with open("model_config.ini", "r") as f:
        config_ini = f.read()
    print(config_ini)

    channel = grpc.insecure_channel('yourip:port')
    stub = model_service_pb2_grpc.ModelServiceStub(channel)
    request = model_management_pb2.ReloadConfigRequest()  ##message ReloadConfigRequest
    model_server_config = model_server_config_pb2.ModelServerConfig()
    x = text_format.Parse(text=config_ini, message=model_server_config) # 非官方认证的方法
    x = text_format.MessageToString(model_server_config)
    with open("x.txt", "w+") as f:
        f.write(x)
    print(x)
    print(model_server_config.IsInitialized())
    request.config.CopyFrom(model_server_config)
    # print(request.ListFields())
    responese = stub.HandleReloadConfigRequest(request, 10)
    if responese.status.error_code == 0:
        print("reload sucessfully")
    else:
        print("reload error!")
        print(responese.status.error_code)
        print(responese.status.error_message)

def read_add_rewrite_config():
    """
    测试读取一个config文件，新加一个配置信息，并且reload过后回写
	test:read a config_file and add a new model, then reload and rewrite to the config_file
    :return:
    """
    with open("model_config.ini", "r") as f:
        config_ini = f.read()
    #print(config_ini)
    model_server_config = model_server_config_pb2.ModelServerConfig()
    model_server_config = text_format.Parse(text=config_ini, message=model_server_config)
    one_config = model_server_config.model_config_list.config.add() # add one more config
    one_config.name = "test2"
    one_config.base_path = "/home/sparkingarthur/tools/tf-serving-custom/serving/my_models/test2"
    one_config.model_platform = "tensorflow"

    print(model_server_config)

    channel = grpc.insecure_channel('10.200.24.101:8009')
    stub = model_service_pb2_grpc.ModelServiceStub(channel)
    request = model_management_pb2.ReloadConfigRequest()
    request.config.CopyFrom(model_server_config)
    responese = stub.HandleReloadConfigRequest(request, 10)
    if responese.status.error_code == 0:
        print("reload sucessfully")
    else:
        print("reload error!")
        print(responese.status.error_code)
        print(responese.status.error_message)
    new_config = text_format.MessageToString(model_server_config)
    with open("model_config.ini", "w+") as f:
        f.write(new_config)
#run_reload_one_config()
#parse_config_file()
read_add_rewrite_config()