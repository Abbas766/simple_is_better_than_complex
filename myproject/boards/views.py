from django.shortcuts import render,get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from boards.models import Board

def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
        print(board.name)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})

def new_topic(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request,'new_topic.html',{'board':board})