from  flask import *
from brownie import smart_lottery,config, network
from scripts.help_scripts import get_accounts, get_contract, fund_with_link
import time

app = Flask(__name__)

account = get_accounts(None, 'samir-account')
def deploy_lottery():
    
    # usd=get_contract("eth_usd")
    # vrfcoordinta =get_contract("VRFCoordinator")

    smart_lottery.deploy(get_contract("eth_usd"),
                               get_contract("VRFCoordinator"),
                               get_contract('Link_Token') ,
                               config["networks"][network.show_active()]["fee"],
                               config["networks"][network.show_active()]["keyhash"],
                               {"from":account},
                               publish_source= config["networks"][network.show_active()].get("verfiy",False)
                               )
    # print(usd, vrfcoordinta,)

def start__lottery():
    
    lottery = smart_lottery[-1]
    start_lottery=lottery.start_lottery({"from":account})
    start_lottery.wait(1)
    print("lottery is started !!! \n welcome to lottery try your luck here??")

def enter_fee():
    
    lottery = smart_lottery[-1]
    Values = lottery.getenterancefee()+100000000
    enter_tx = lottery.enter({"from":account,"value":Values})
    enter_tx.wait(1)
    print("You paid fee")

def end_lottery():
    
    lottery= smart_lottery[-1]
    #fund
    tx= fund_with_link(lottery)
    tx.wait(1)
    end_lottery = lottery.end_lottery({"from":account, 'gas_limit': 6721975,"allow_revert":False})
    end_lottery.wait(1)
    time.sleep(60)
    print(f"{lottery.winner()} is new winner")

def main():
    deploy_lottery()
    start__lottery()
    enter_fee()
    end_lottery()