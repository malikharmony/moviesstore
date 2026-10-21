from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Report, Ratings
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    ratings = Ratings.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews

    total = 0
    count = 0
    for rating in ratings:
        total += int(rating.score)
        count += 1

    if count > 0:
        average = float(total) / count
        template_data['average_rating'] = average
    else:
        template_data['average_rating'] = 0.0

    if request.user.is_authenticated:
        template_data['user_rating'] = Ratings.objects.filter(movie=movie, user=request.user)

    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Report Review'
        return render(request, 'movies/report_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['reason'] != '':
        report = Report()
        report.reason = request.POST['reason']
        report.comment = review.comment
        report.review = review
        report.user = request.user
        report.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def create_rating(request, id):
    if request.method == 'POST':
        score = request.POST['score']
        if score is not None:
            movie = get_object_or_404(Movie, id=id)
            rating = None
            try:
                rating = Ratings.objects.get(movie=movie, user=request.user)
            except:
                rating = None

            if rating is None:
                rating = Ratings()
                rating.movie = movie
                rating.user = request.user

            rating.score = int(score)
            rating.save()
    return redirect('movies.show', id=id)
    










# @login_required
# def create_review(request, id):
#     if request.method == 'POST' and request.POST['comment'] != '':
#         movie = Movie.objects.get(id=id)
#         review = Review()
#         review.comment = request.POST['comment']
#         review.movie = movie
#         review.user = request.user
#         review.save()
#         return redirect('movies.show', id=id)
#     else:
#         return redirect('movies.show', id=id)