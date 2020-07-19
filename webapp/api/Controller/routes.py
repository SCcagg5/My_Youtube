from .routesfunc import *

def setuproute(app, call):
    @app.route('/',                 ['OPTIONS', 'GET'],         lambda x = None: call([])                                            )
    @app.route('/user',    	        ['OPTIONS', 'POST'],        lambda x = None: call([signup])                                      )
    @app.route('/validate',         ['OPTIONS', 'POST'],        lambda x = None: call([verifykey, get_token])                         )
    @app.route('/auth',    	        ['OPTIONS', 'POST'],        lambda x = None: call([signin, check_act, get_token])                )
    @app.route('/user/<>',    	    ['OPTIONS', 'DELETE'],      lambda x = None: call([authuser, delete_user])                       )
    @app.route('/user/<>',    	    ['OPTIONS', 'PUT'],         lambda x = None: call([authuser, modify_user, get_token])            )
    @app.route('/user/<>',    	    ['OPTIONS', 'GET'],         lambda x = None: call([authuser, get_user])                          )
    @app.route('/users',        	['OPTIONS', 'GET'],         lambda x = None: call([get_all_users])                               )
    @app.route('/user/<>/video',    ['OPTIONS', 'POST'],        lambda x = None: call([authuser, post_video])                        )
    @app.route('/user/<>/videos',   ['OPTIONS', 'GET'],         lambda x = None: call([get_videos])                                  )
    @app.route('/video/<>',         ['OPTIONS', 'PATCH'],       lambda x = None: call([authuser, patch_video])                       )
    @app.route('/video/<>',         ['OPTIONS', 'PUT'],         lambda x = None: call([authuser, modify_video])                      )
    @app.route('/video/<>',         ['OPTIONS', 'DELETE'],      lambda x = None: call([authuser, delete_video])                      )
    @app.route('/videos',        	['OPTIONS', 'GET'],         lambda x = None: call([get_all_videos])                              )
    @app.route('/video/<>/comment', ['OPTIONS', 'POST'],        lambda x = None: call([authuser, post_comment])                      )
    @app.route('/video/<>/comment', ['OPTIONS', 'GET'],         lambda x = None: call([get_comment])                                 )
    @app.route('/admin/login/',     ['OPTIONS', 'POST'],        lambda x = None: call([admtoken])                                    )
    @app.route('/admin/allusers/',  ['OPTIONS', 'GET'],         lambda x = None: call([authadmin, all_users])                        )
    @app.route('/admin/spoof/',     ['OPTIONS', 'POST'],        lambda x = None: call([authadmin, gettokenadm])                      )
    def base():
        return
