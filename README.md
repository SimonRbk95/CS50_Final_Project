# CS50 Final Project — Online Digital Skills Consultant
Information technologies are still very foreign for many people working in various industries. Either reskilling or improving existing technical skills will be critical for people to be competitive in the market. Fortunately, there are many hands-on courses online that facilitate just that. However, the supply is overwhelming with thousands of these courses. The online digital skills consultant solves this problem by suggesting personalized courses from Coursera and free relevant Youtube videos that help get a first overview of the field of interest.

The Flask web application uses Python for routing and creating the logic behind suggesting courses, Javascript for interactive buttons and forms, HTML, CSS, and Jinja 2 to create HTML dynamically.

###
Technologies used:
- Flask (as a framework)
- Python
- Javascript
- Jinja2
- HTML
- CSS
- other small libraries or packages

### Video URL
https://youtu.be/G8JI2XQakN4

# How does it work:

## User input:
The users gets prompted by a Get Started button that takes them to a questionnaire. All these mandatory questions serve to determine which courses and videos to suggest.

1. How comfortable are you with basic technologies?
2. How comfortable are you with programming?</br>
    <sub>The first two questions can be answered with less, more, and very. Each answer triggers different keywords used to fetch video IDs via Youtube's data search API.
3. What are your areas of interest?</br>
    <sub>The third question is a multiple-choice one, currently restricted to a maximum choice of three areas of interest. This arbitrary restriction serves only to avoid having a results page so long as to be offputting for the user.

4. What are your goals?</br>
    <sub>The fourth question determines the user's goals, influencing the type of suggested courses.

All the answers are stored in Python Lists and dynamically allocated via Jinja2, ensuring easy maintenance and enabling course suggestions.

## Coursera Database:
Access to Coursera courses is granted by getting access to their affiliated program. Then you can browse their courses and download their course catalogues. For the application, I use their Top 100-course catalogue and a file comprising 5000 tech courses pre-sorted by relevance. Both course catalogues come in different file formats and comprise slightly different information, which has to be accounted for in working with them. Also, Coursera does not provide a simple API; the course databases may be updated manually by downloading their catalogue once in a while. For these reasons, in helpers.py, I have adjusted the functions "read_txt" and "read_csv". This way, the course files only need to be downloaded, named cdb and cdb_100, and placed in the project folder for it to work. These functions load up the course databases into dictionaries that are needed to suggest the courses.

## Parameters used to look for courses:
To look for courses, questions 3 and 4 are critical. Question 3 returns the choices' indices. These indices correspond to a list containing keywords. These keywords will be used to search for matches. Currently, only the first answer to question 4 impacts the course suggestion by prioritizing a particular Coursera product type that aligns with the user's goal of starting a new career in tech.

## Querying the Coursera databases:
The Top 100 database is searched first, storing information about the course in a dictionary. For these matches, the more extensive database can provide further information, such as thumbnails and a course description. If the top 100 database does not satisfy the maximum number of suggested courses, the algorithm will query the larger Coursera database for more options. Eventually, the algorithm creates a list that, for each answer to question 3, contains a list of dictionaries with relevant courses.

## Youtube Videos via its API:
Very straightforward, based on a list of keywords for every possible area of interest, one function fetches the video IDs from Youtube's API to suggest relevant courses in English at medium length. Currently, the API Key is retrieved via the OS environment.

## Final display of course suggestions:
Jinja2 uses the python variables to dynamically create the html files displaying all the course and video suggestions, avoiding as much hard-coded HTML as possible.

# Further improvements
- Access to other course vendors' databases, such as via edX's API or Udacity's affiliated program, would bring more variety to the selection. The code is already adjusted to add other course vendors. The only thing that likely needs adjustment is the search algorithm, as different vendors will have different keys and may provide dissimilar information on their courses. Also, access to their databases requires an application on their websites.
- Youtube has a daily quota on data API requests. Therefore, extensive usage of this web application might need a fallback to a pre-stored set of video ids.



