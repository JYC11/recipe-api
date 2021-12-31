# recipe-api

This was a project I did while following a udemy course.

## New things I learnt:
1. There are many ways to organize a django project
2. Class based views have a time and place
3. How to do TDD with django

## Things that weren't new but was good practice:
* overall django concepts(project, apps, admin, models, views, etc)

## More elaboration on the new stuff I learnt:
1. There are many ways to organize a django project
* You can put all the models in one app as opposed to each app having a separate model(how this project was done)
* You can not use different apps at all and put everything in one app(kinda weird, not how this project was done)
* How you organize your django project really depends on your project needs and how the project is gonna scale

2. Class based views
* For very simple CRUD stuff, class based views are very useful as you can just import it and implement CRUD in 2 lines of code
* For very custom business logic, it would be better to use function based views instead of the basic class based views
* Class based views can end up obscuring a lot of the stuff under the hood and personally (coming from node.js) I did not like it too much even though it meant I didn't have to write all the code
* If you don't know too much about Django then this may be bad(my case)
* I'll aim to use function based views from now on until I really need to use class based views(ideally I would like to use a mix)

3. TDD with Django
* Got a very thorough practice at how to implement TDD for the entirety of the django project
* You can just about test everything

## Things I would like to learn more about
I naively thought that I would be sorta good enough for a django take home asessment after all this studying.

But it turns out that there is just so much more to django than I initially thought because I got absolutely wrecked.

It turns out I do not know much about the django ORM so that I will probably have to learn more about.

2 scoops of Django is another thing I'm interested in because it deals with the best practices when doing a django project.

Since there are so many ways to actually implement a django project, I got decision paralysis so reading the book would be pretty interesting.
