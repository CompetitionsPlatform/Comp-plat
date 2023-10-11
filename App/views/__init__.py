# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .competition import comp_views
from .profile import profile_views
from .ranking import ranking_views


views = [user_views, index_views, auth_views, comp_views, profile_views, ranking_views]
# blueprints must be added to this list