from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse, QueryDict
##普通参数的接收⽅法
# def index(request):
#     year = request.GET.get("year","2019")
#     month = request.GET["month"]
#     #return HttpResponse("<p>Hello word, Hello, Django</p>")
#     return HttpResponse("year is %s,month is %s" % (year,month))
##关键字传参
#def index(request, **kwargs):
   # print(kwargs)
    # year = kwargs.get('year', 2018)
    # month = kwargs.get('month', 7)
    #year = kwargs.get('year')
    #month = kwargs.get('month')
    # return HttpResponse("year is %s,month is %s" %(year,month))
    #return HttpResponse("<p>year-{} , month-{}</p>".format(year, month))
# def index(request,year=2018,month=8):
#     return HttpResponse("year is %s,month is %s" % (year,month))

# 请求参数接收，默认为GET请求，通过method判断POST请求
# def index(request):
#      print(request.scheme)
#      print(request.method)
#      print(request.headers)
#      print(request.path)
#      print(request.META)
#      print(request.GET)
#      data = request.GET
#      year = data.get("year", "2019")
#      month = data.get("month", "10")
#      if request.method == "POST":
#          print(request.method)
#          print(request.body)
#          print(QueryDict(request.body).dict())
#          print(request.POST)
#          data = request.POST
#          year = data.get("year","2018")
#          month = data.get("month", "07")
#      return HttpResponse("year is %s,month is %s" % (year,month))
# def index(request):
#     classname = "DevOps"
#     books = ['Python', 'Java', 'Django']
#     user  ={'name':'kk','age':18}
#     userlist =  [ {'name':'kk','age':18}, {'name':'rock','age':19},
# {'name':'mage','age':20}]
#
#     return render(request, "hello/hello.html",{'aa':classname,"books":books,"user":user,"userlist":userlist})

#list user
def list(request):
    users = [
            {'username': 'kk1', 'name_cn': 'kk1', 'age': 18, 'sex':'男'},
            {'username': 'kk2', 'name_cn': 'kk2', 'age': 19, 'sex':'女'},
            {'username': 'kk3', 'name_cn': 'kk3', 'age': 20, 'sex':'男'},
    ]
    print(users)
    return render(request, 'hello/userlist.html', {'users': users})
