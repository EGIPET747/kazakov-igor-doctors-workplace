from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.template import loader
import logging
from project.models import Person, Examination, Symptom, Disease

dt_now = datetime.now()
dt_now = f'{dt_now.year}{"0" + str(dt_now.month) if dt_now.month < 10 else dt_now.month}' \
         f'{"0" + str(dt_now.day) if dt_now.day < 10 else dt_now.day}'
logging.basicConfig(level=logging.INFO, filename=f'doctors_workplace-{dt_now}.log', format='%(asctime)s %(levelname)s:%(message)s')


def home(request, doc_id):
    template = loader.get_template('main_page.html')
    persons = [{'fio': 'ВЫБЕРИТЕ ПАЦИЕНТА', 'height': 0, 'id': 0, 'passport': 0, 'oms': 0}]
    persons_all = Person.objects.all()
    symptoms = Symptom.objects.all()
    persons.extend(
        [{'fio': p.fio, 'height': p.height, 'id': p.id, 'passport': p.passport, 'oms': p.oms} for p in persons_all])
    context = {
        'doc_id': doc_id,
        'persons': persons,
        'symptoms': [{'name': s.name, 'id': s.id} for s in symptoms]
    }
    logging.info(f'home_page success. doc_id: {doc_id}')
    return HttpResponse(template.render(context, request))
    # return HttpResponse(f"Home page for doc {doc_id}")


def get_history(request):
    if request.method == 'POST':
        try:
            person_id = request.POST.get('person_id')
            examinations = Examination.objects.filter(person_id=person_id)
            examinations = [{
                'datetime': e.datetime,
                'description': e.description,
                'symptoms': [s.name for s in e.symptoms.all()],
                'person_id': e.person_id.fio,
                'diseases': ', '.join([d.name for d in e.diseases.all()])
            } for e in examinations]
            response = {'examinations': examinations}
            logging.info(f'get_history success. count of examinations: {len(response["examinations"])}')
            return JsonResponse(response)
        except Exception as e:
            logging.warning(f"warning. get_history: {e.__class__}")
    logging.warning("warning. query get_history not POST")
    return JsonResponse({'warning': 'not POST'})


def get_disease(request):
    if request.method == 'POST':
        try:
            symptoms = request.POST.get('symptoms')
            symptoms = symptoms.split(',')
            if isinstance(symptoms, list):
                symptoms = [int(s) for s in symptoms]
            else:
                symptoms = [int(symptoms)]
            diseases = Disease.objects.filter(symptoms__id__in=symptoms)
            diseases = [{
                'id': d.id,
                'name': d.name,
                'description': d.description,
                'symptoms': [s.name for s in d.symptoms.all()],
            } for d in diseases]
            diseases = list({d['id']: d for d in diseases}.values())
            response = {'diseases': diseases}
            logging.info(f'get_disease success. count of diseases: {len(response["diseases"])}')
            return JsonResponse(response)
        except Exception as e:
            logging.warning(f"warning. get_disease: {e.__class__}")
    logging.warning("warning. query get_disease not POST")
    return JsonResponse({'warning': 'not POST'})


def save_exam(request):
    if request.method == 'POST':
        try:
            symptoms = request.POST.get('symptoms')
            symptoms = symptoms.split(',')
            if isinstance(symptoms, list):
                symptoms = [int(s) for s in symptoms]
            else:
                symptoms = [int(symptoms)]
            diseases = request.POST.get('diseases')
            diseases = diseases.split(',')
            if isinstance(diseases, list):
                diseases = [int(d) for d in diseases]
            else:
                diseases = [int(diseases)]
            person_id = int(request.POST.get('person_id'))
            description = request.POST.get('description')
            time = request.POST.get('time')
            logging.log(level=1, msg='all is ok')
            t = datetime.strptime(time, '%d.%m.%Y %H:%M:%S')
            person = Person.objects.get(id=person_id)
            symptoms = Symptom.objects.filter(id__in=symptoms)
            diseases = Disease.objects.filter(id__in=diseases)
            e = Examination.objects.create(
                datetime=t,
                description=description,
                person_id=person,
            )
            for s in symptoms:
                e.symptoms.add(s)
            for d in diseases:
                e.diseases.add(d)
            e.save()
            response = {'success': 'ok'}

            logging.info(f'save_exam success.')
            return JsonResponse(response)
        except Exception as e:
            logging.warning(f"warning. save_exam: {e.__class__}")
    logging.warning("warning. query save_exam not POST")
    return JsonResponse({'warning': 'not POST'})
