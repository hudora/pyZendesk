# pyZendesk - a Python module for zendesk.com

pyZendesk is a Python module for zendesk.com.
pyZendesk allows you to
1. create new users
2. create signed links


## Configuration
The configuration of pyZendesk are the following variables:
Set DESK_URL to the url of your zendesk account:
    DESKURL = 'http://yoursubdomain.zendesk.com/'

If you want to create new users, you must set the environment variable **ZENDESK\_CREDENTIALS**.
If you want to create links, you must set the environment variable **ZENDESK\_REMOTE\_AUTH\_TOKEN**.

## Enable remote authentication
Remote authentication can be enabled at https://yoursubdomain.zendesk.com/account/security
See http://www.zendesk.com/api/remote-authentication for further instructions.

## Examples

Create a new user:
    os.environ['ZENDESK_DOMAIN'] = 'example'
    os.environ['ZENDESK_CREDENTIALS'] = 'username@example.com:secret'
    
    import zendesk
    zendesk.create_user('Joe Average', 'joe@example.com')

Create a signed link:

    os.environ['ZENDESK_DOMAIN'] = 'example'
    os.environ['ZENDESK_REMOTE_AUTH_TOKEN'] = 'TOKEN'
    zendesk.create_link('Joe Average', 'joe@example.com')
