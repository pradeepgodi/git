import requests
import datetime

'''
SONYLIV : CMS API request 
QA : https://7dd67fc2.cdn.cms.movetv.com/cms/api/channels/d8a98b9bd26d4986a799435c68f2f89e/network
BETA : https://93a256a7.cdn.cms.movetv.com/cms/api/channels/693aaf3bc0a14419aef7cafc9173560f/network
PROD : https://cbd46b77.cdn.cms.movetv.com/cms/api/channels/6de69ceadafa46ce929105cb26275b31/network
'''

# Enter environment values for assets comparison values = 'QA','BETA','PROD'
env_list = ['QA', 'BETA', 'PROD']  # uncomment the line to compare between QA,BETA and PROD
# env_list =['QA','BETA']       # uncomment the line to compare between QA,BETA
# env_list = ['PROD']           # uncomment to get details on one Environment QA or BETA or PROD


# SONYLIV_<env> = [<CMS_ID>,<NETWORK_ID>]
SONYLIV_QA = ['7dd67fc2', 'd8a98b9bd26d4986a799435c68f2f89e']
SONYLIV_BETA = ['93a256a7', '693aaf3bc0a14419aef7cafc9173560f']
SONYLIV_PROD = ['cbd46b77', '6de69ceadafa46ce929105cb26275b31']

# to collect ribbon details
ribbons_count_list = []  # to collect the count of ribbons in each environment e.g [8,7,9]
ribbons_count_dict = {}  # to collect count of ribbons in environment e.g {'QA': 8, 'BETA': 7}
ribbon_title_dict = {}   # to collect env and its ribbons name {'QA':[u'SET', u'SAB', u'Web Originals'}


def get_network(cms_id, network_id):
    url = 'https://' + cms_id + ".cdn.cms.movetv.com/cms/api/channels/" + network_id + "/network"
    try:
        response = requests.request("GET", url)
        response_list = response.json()
        request_status = response.status_code
        return request_status, response_list, url
    except ValueError,requests.exceptions.ConnectionError:
        print("Network request caught exception.Check the network or url.")


def get_ribbon_titles(env,response):
    title_list = []
    for count in range(0, len(response)):
        # print response[count]["title"]
        title_list.append(response[count]["title"])
    ribbon_title_dict[env] = title_list


def get_ribbons_count(env,status,response,url):
    print "Requesting " + env + " Network ->"
    if status == 200:
        number_of_ribbons = len(response)
        # print('Number for ribbons : ', number_of_ribbons)
        ribbons_count_dict[env] = number_of_ribbons
        ribbons_count_list.append(number_of_ribbons)
        get_ribbon_titles(env, response)
    else:
        print(env+" Network Request Failed :", status)


def compare_ribbons():
    for env in env_list:
        if env == 'QA':
            status, response, url = get_network(SONYLIV_QA[0], SONYLIV_QA[1])  # get_network(cms_id,network_id)
            get_ribbons_count(env,status, response,url)
        elif env == 'BETA':
            status, response, url = get_network(SONYLIV_BETA[0], SONYLIV_BETA[1])
            get_ribbons_count(env, status, response, url)
        elif env == 'PROD':
            status,response,url = get_network(SONYLIV_PROD[0], SONYLIV_PROD[1])
            get_ribbons_count(env, status, response, url)

    print "\n[************* RESULT [SONY LIV] ********************]\n"
    if (len(set(ribbons_count_list)) == 1) & (len(ribbons_count_list) > 1):
        print "A] RIBBONS COUNT MATCH  : ", ribbons_count_list[0]
    elif len(ribbons_count_list) == 1:
        print "A] RIBBON COUNT IN " + env + " : ", ribbons_count_dict[env]

    else:
        print "A] RIBBONS COUNT DON'T MATCH : ", ribbons_count_dict
# Print all  ribbon names in the environment
    for keys in ribbon_title_dict:
        ribbon_name = u",".join(ribbon_title_dict[keys])
        print "\t\t"+keys + " ribbons: ", ribbon_name


def main():
    start_time = datetime.datetime.now()
    compare_ribbons()

    end_time = datetime.datetime.now()
    print "\n\nTime taken by the script : ", end_time-start_time


if __name__ == '__main__':
    main()
