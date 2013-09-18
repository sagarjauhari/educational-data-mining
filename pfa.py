import csv
import math


SR = 0
kcdict={}
gamma_kc = []
rho_kc = []
student_obj_dict={}
beta = 0.5
sr_list = []

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap

def init_gamma_rho():
	for i in xrange(0,len(kcdict)):
		gamma_kc.append(0.5)
		rho_kc.append(0.5)

def createKCList():
	id = 0
	with open('kclist.csv','rb') as csvfile:
		KCreader = csv.reader(csvfile, delimiter=',')
		for row in KCreader:
			kcdict[row[0]] = id
			id = id+1

class Student:
	gamma = [0] * len(kcdict)
	rho = [0] * len(kcdict)
	success_param = 0
	fail_param = 0

def update_student(student, right, kc):
	if right == 1:
		student_obj_dict[student].gamma[kc] = student_obj_dict[student].gamma[kc] + gamma_kc[kc]
	else:
		student_obj_dict[student].rho[kc] = student_obj_dict[student].rho[kc] + rho_kc[kc]
	student_obj_dict[student].success_param = sum(student_obj_dict[student].gamma)
	student_obj_dict[student].fail_param = sum(student_obj_dict[student].rho)

def do_pfa():
	with open('Asgn1dataset.csv','rb') as csvfile:
		inputreader = csv.reader(csvfile, delimiter=',')
		for row in inputreader:
			idd = row[0]
			lesson = row[1]
			student = row[2]
			kc = kcdict[row[3]]
			item = row[4]
			right = row[5]
			first_att = row[6]
			time = row[7]

			if student in student_obj_dict:
				update_student(student, right, kc)			
			else:
				student_obj_dict[student] = Student()
				student_obj_dict[student].gamma = [0] * len(kcdict)
				student_obj_dict[student].rho = [0] * len(kcdict)
				update_student(student, right, kc)
			m = student_obj_dict[student].success_param + student_obj_dict[student].fail_param + beta
			p = 1 / (1 + math.exp(-m))
			sr = math.pow((p - int(right)),2)*int(first_att)
			sr_list.append(sr)
	print(sum(sr_list))

def do_optimization():
	for beta in [x/10 for x in xrange(-10,10)]:
		for gamma in [y/10 for y in xrange(-10,10)]:
			for rho in [z/10 for z in xrange(-10,10)]:
				do_pfa()

createKCList()
init_gamma_rho()
do_optimization()
