from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.url import route_url

from ocn.models import DBSession
from ocn.models import Subject
from ocn.models import Section
from ocn.models import Paragraph
from ocn.models import Comment

def view_home(request):
    # Simple redirect to the home page in the static folder
    sublistlink = route_url('subject_list', request)
    return dict(subjectlistlink = sublistlink)

def view_subject_list(request):
    """ Show a list of all subjects for which there are notes available. """
    session  = DBSession()
    subjects = session.query(Subject).all()
    # Link back to home page
    homelink = route_url('home', request)
    # Pairs of (Subject Name, URL), used to construct subject links in template
    link_info = []
    for s in subjects:
        # URLs generated by route_url relative to the last request
        url = route_url('subject_index', request, subjectcode=s.code)
        link_info.append((s.name, url))
    return dict(link_info=link_info, homelink=homelink)

def view_subject_index(request):
    """ Show a list of all sections in the notes for a specific subject. """
    session     = DBSession()
    # Subject code; e.g. 'mast30025'
    subjectcode = request.matchdict['subjectcode']
    subject     = session.query(Subject).filter_by(code=subjectcode).one()
    # List of Section objects associated (by foreign key) with the subject
    sections    = subject.sections
    # (Section Name, URL) pairs to construct the links to sections in template
    link_info = []
    for s in sections:
        # URLs generated by route_url relative to the last request
        url = route_url('section', request, subjectcode=subjectcode,
                                            sectionurlname=s.url)
        link_info.append((s.name, url))
    return dict(link_info   = link_info,
                subjectname = subject.name,
                subjectcode = subject.code)

def view_section(request):
    """ Show a specific section in a subject; display the paragraphs
        in that section followed by their comment sections. """
    session = DBSession()

    subjectcode    = request.matchdict['subjectcode']
    sectionurlname = request.matchdict['sectionurlname']

    # Get the section object we are trying to view
    section = session.query(Section) \
                     .filter_by(subject_code=subjectcode, url=sectionurlname) \
                     .one()

    # The paragraphs associated with that section
    paragraphs = section.paragraphs
    
    # Pairs of (Paragraph HTML, Comment List) to render
    c_p_pairs = []
    for p in paragraphs:
        # Get an ordered list of comment objects associated with a given paragraph
        comments = session.query(Comment).filter_by(paragraph_id=p.id) \
                                         .order_by(Comment.datetime).all()
        c_p_pairs.append((p.html,comments))

    return dict(c_p_pairs=c_p_pairs,
                sectionname=section.name)

# A separate view for comments will be necessary if these are to be
# loaded on-the-fly using jQuery
#def view_comments(request):