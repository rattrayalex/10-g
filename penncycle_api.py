import random, json, hashlib, hmac, gviz_api, operator, math, csv, xlwt, datetime
from collections import Counter
from django.http import HttpResponseRedirect, HttpResponse
from app.models import *
from django.db.models.loading import get_model, get_models, get_app
from django.template.defaultfilters import slugify
from django.utils import encoding
from django.contrib.auth.decorators import login_required

def signups(request):
  print 'in get_stats'
  students = Student.objects.all()#.order_by(join_date)
  description = [
    ('date', 'date','Signup Date'),
    ('signups','number','Signups'),
    ('cum','number','Cumulative'),
    ]
  data = Counter([s.join_date for s in students]).items()
  data = sorted(data, key=operator.itemgetter(0), reverse=False)
  print data
  n=0
  longdata = []
  for d in data:
    n+=d[1]
    longdata.append(d+(n,))
  print longdata
  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(longdata)
  json = data_table.ToJSon(columns_order=("date", "signups", "cum"), order_by="date")

  return HttpResponse(json, content_type="application/json")

def schools(request):
  students = Student.objects.all()
  description = [
    ('school','string','School'),
    ('count','number','Count'),
    ]
  columns_order = ('school', 'count')
  order_by = columns_order[1]
  data = Counter([s.school for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def majors(request):
  students = Student.objects.all()
  description = [
    ('major','string','Major'),
    ('count','number','Count'),
    ]
  columns_order = ('major', 'count')
  order_by = columns_order[1]
  data = Counter([s.major for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def numrides(request):
  students = Student.objects.all()
  description = [
    ('numrides','string','Number of Rides'),
    ('frequency','number','Frequency'),
    ]
  columns_order = ('numrides', 'frequency')
  order_by = columns_order[0]

  def num_rides(student):
    return len(student.ride_set.all())

  data = Counter([num_rides(s) for s in students]).items()

  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

@login_required
def emails(request):
  students = Student.objects.all()
  string = ', '.join([s.email for s in students])
  return HttpResponse(string)

def duration(request):
  print 'in duration function'
  rides = Ride.objects.all()
  print 'got rides'
  description = [
    ('duration','string','Duration of Rides'),
    ('count','number','Count'),
    ]
  columns_order = ('duration', 'count')
  order_by = columns_order[0]
  # here i basically make my own map because a dict is immutable. better way to do this?
  keyList = [float(t)/2 for t in range(0, 21, 1)]
  keyList.append('more')
  valList = [0 for i in range(0, 22, 1)]
  for r in rides:
    if r.checkin_time != None:
      rideDuration = r.checkin_time - r.checkout_time
      hours = math.floor((float(rideDuration.seconds) / 3600) * 2) / 2
      if hours > 10.0:
        hours = 'more'
      index = keyList.index(hours)

      valList[index] = valList[index] + 1
      print valList[index]

  # put all that shit back into a dict
  print 'making data'
  #data = {{float(t)/2: valList[valList.index(float(t)/2)]} for t in range(0, 21, 1)}
  data = []
  for i in range(len(keyList)):
    tempTuple = (keyList[i], valList[i])
    data.append(tempTuple)

  #data = Counter([num_rides(r) for r in rides]).items()

  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def gender(request):
  students = Student.objects.all()
  description = [
    ('gender','string','Gender'),
    ('count','number','Count'),
    ]
  columns_order = ('gender', 'count')
  order_by = columns_order[1]
  data = Counter([s.gender for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def housing(request):
  students = Student.objects.all()
  description = [
    ('housing','string','Housing'),
    ('count','number','Count'),
    ]
  columns_order = ('housing', 'count')
  order_by = columns_order[1]
  data = Counter([s.living_location for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def paid(request):
  students = Student.objects.all()
  description = [
    ('paid','string','Has Paid?'),
    ('count','number','Count'),
    ]
  columns_order = ('paid', 'count')
  order_by = columns_order[1]
  data = Counter([s.paid for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def year(request):
  students = Student.objects.all()
  description = [
    ('year','string','Year'),
    ('count','number','Count'),
    ]
  columns_order = ('year', 'count')
  order_by = columns_order[1]
  data = Counter([s.grad_year for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def waived(request):
  students = Student.objects.all()
  description = [
    ('waived','string','Signed Waiver?'),
    ('count','number','Count'),
    ]
  columns_order = ('waived', 'count')
  order_by = columns_order[1]
  data = Counter([s.waiver_signed for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def payment(request):
  students = Student.objects.all()
  description = [
    ('payment','string','Type of Payment'),
    ('count','number','Count'),
    ]
  columns_order = ('payment', 'count')
  order_by = columns_order[1]
  data = Counter([s.payment_type for s in students]).items()
  #data = sorted(data, key=operator.itemgetter(0), reverse=True)
  print data
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

def checkouts(request):
  print 'in get_stats'
  rides = Ride.objects.all()
  description = [
    ('date', 'date','Checkout Date'),
    ('checkouts','number','Checkouts'),
    ('cum','number','Cumulative'),
    ]
  columns_order = ('date', 'checkouts', 'cum')
  order_by = columns_order[0]
  data = Counter([r.checkout_time.date() for r in rides]).items()
  data = sorted(data, key=operator.itemgetter(0), reverse=False)
  print data
  n=0
  longdata = []
  for d in data:
    n+=d[1]
    longdata.append(d+(n,))
  print longdata
  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(longdata)
  json = data_table.ToJSon(columns_order=columns_order, order_by=order_by)

  return HttpResponse(json, content_type="application/json")

@login_required
def dump(request):
  response = HttpResponse(mimetype="application/ms-excel")
  response['Content-Disposition'] = 'attachment; filename=PennCycle-Database-Dump-%s.xls' % (str(datetime.datetime.today()))

  wb = xlwt.Workbook()
  excel_date_fmt = 'M/D/YY h:mm'
  datestyle = xlwt.XFStyle()
  datestyle.num_format_str = excel_date_fmt
  plainstyle = xlwt.XFStyle()

  app = get_app('app')
  models = get_models(app)

  for model in models:
    name = model.__name__
    print name
    if name == 'Plan':
      break
    ws = wb.add_sheet(slugify(name))
    xl_export(model, ws, datestyle, plainstyle)

  wb.save(response)
  return response

def xl_export(model, ws, datestyle, plainstyle):
  fields = model._meta.fields
  headers = [f.name for f in fields]
  for colx, val in enumerate(headers):
    ws.write(0, colx, val)
  queryset = model.objects.all()
  for rowx, obj in enumerate(queryset):
    for colx, field in enumerate(headers):
      if field in headers:
        val = getattr(obj,field)
        print type(val)
        if callable(val):
          val = val()
        # val = encoding.smart_str(val, encoding='ascii', errors='ignore')
        print type(val)
        fieldtype = fields[colx].get_internal_type()
        if fieldtype in ['IntegerField', 'FloatField', 'AutoField']:
          print "It's an number!"
          val = float(val)
        if fieldtype in ['ForeignKey', 'ManyToMany', 'OneToOne','ImageField','FileField']:
          val = str(val)
        if fieldtype == 'DateTimeField':
          thisstyle = datestyle
        else:
          thisstyle = plainstyle
        print fieldtype
      ws.write(rowx+1,colx,val, thisstyle)
  return None