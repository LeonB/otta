# Online Time Tracking App #

# Requirements #
* pip install jira-python pypubsub

# Example shell #
> otta start
> What project, Dave?
> What To-do Item?
> otta stop|start

Timer
Backend
Service (BC, JIRA)

Backend.get_projects()
Backend.get_todo_items()
Backend.log_time(time, project = None, todo_item = None)

Config.services.jira
Config.

http://www.myintervals.com/blog/wp-content/uploads/2011/03/time-tracking-on-the-mac-with-eon-01.jpg
https://www.google.nl/webhp?sourceid=chrome-instant&ie=UTF-8#hl=nl&output=search&sclient=psy-ab&q=appindicator%20%22set_label%22&oq=&gs_l=&pbx=1&fp=80a4400568980b6&bav=on.2,or.r_gc.r_pw.r_cp.r_qf.&biw=1920&bih=947

Global idea:
  - worktimers: van/tot/project/todo/active (kan maar 1 active zijn)
  -

@todo:
  - When away: stop timer
  - think about how/when to post
  - seperate class for upload function
  - Make it workspace dependant (hamster)
  - Notifications
  - Respect gnome date format
  - Alleen projecten met actieve todo items (# in haakjes?)

Away function
  - http://live.gnome.org/GnomeScreensaver/FrequentlyAskedQuestions#Is_there_a_way_to_perform_actions_when_the_screensaver_activates_or_deactivates.3F__Or_when_the_session_becomes_idle.3F
  - use idle.py from project hamster

Inspiration:
  - http://fuelcollective.com/images/eon/screenshots/screenshot.png
  - http://mac.appstorm.net/wp-content/uploads/2010/09/05_menu_eon.jpg
  - http://www.gosstech.ca/products/eon/eonimages/eon_formatting.png
  - http://mac.appstorm.net/wp-content/uploads/2010/09/07_edit_times.jpg

GUI/GTK:
  - Provide an access key in all check box labels that allows the user to set or unset the check box directly from the keyboard.
  - Drop-down Combination Boxes: http://library.gnome.org/devel/hig-book/2.32/controls-combo-boxes.html.en
  - http://library.gnome.org/devel/hig-book/2.32/images/visdes-layout-annotated.png.en
  - Spacing and Alignment: 8.2.3 (http://library.gnome.org/devel/hig-book/2.32/design-window.html.en#layout-callouts-figure / http://library.gnome.org/devel/hig-book/2.32/windows-alert.html.en)
  - 1.6:1
  - http://swapoff.posterous.com/decoupling-ui-from-logic-with

Documentation:
  - http://learnpygtk.org/pygtktutorial/spinner.html
  - http://www.eurion.net/python-snippets
  - http://docs.python.org/library/profile.html

DB:
  - http://code.activestate.com/recipes/526618-multithread-support-for-sqlite-access/

Autostart:
  - ~/.config/autostart/
  - http://gdevilspie.googlecode.com/svn-history/r127/trunk/gdevilspie (UpdateAutostartStatus(self))

Opzet classes:
  Project(sqlite) (Deze maar even laten zitten?)
    - BascampProject(BasecampObject) (lxml)
