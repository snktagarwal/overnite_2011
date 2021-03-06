from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from main.models import *
from main import tasks

def home(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES) 
        if form.is_valid():            
            new_submission = form.save()
            new_submission.celery_task = tasks.submit.apply_async(args=[new_submission.name,new_submission.program,new_submission.input_file,new_submission.output_file])
            new_submission.save()
            return HttpResponseRedirect('/'+str(new_submission.id))
    else:
        form = SubmissionForm()
    return render_to_response('main/home.html', {
        'form': form,
    })

def result(request, sub_id):
    submission = get_object_or_404(Submission, pk = sub_id)
    return render_to_response('main/result.html', {
        'submission': submission,
    })
