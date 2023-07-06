


from http.client import LineTooLong
from brownie import accounts,config, network,MockV3Aggregator, VRFCoordinatorMock, Contract, LinkToken, interface, smart_lottery
LOCAL_FORK_DELPOY =["mainnet-fork", "mainnet-fork-dev"]
LOCAL_DEPLOY_CONTRACT =['development', 'ganache-locall','ganach']

def get_accounts(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(network.show_active() in LOCAL_DEPLOY_CONTRACT or network.show_active() in LOCAL_FORK_DELPOY):
        return accounts[0]
    else:
        return config["wallet"]["from_key"]

connect_to_mock = {"eth_usd":MockV3Aggregator,"VRFCoordinator":VRFCoordinatorMock, "Link_Token":LinkToken}

def get_contract(contract_name):
    """to cerate a mock contract
    """
    contract_type = connect_to_mock[contract_name]
    if network.show_active() in LOCAL_DEPLOY_CONTRACT:
        if len(contract_type) <=0:
            deploy_mock()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address,contract_type.abi)
    return contract



DECIMALS = 18
INTIAL_VALUE= 200000000

def deploy_mock(decimal=DECIMALS, intial_value=INTIAL_VALUE):
    account = get_accounts()
    MockV3Aggregator.deploy(decimal,intial_value,{"from":account})
    link_token = LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token,{"from":account})
    print("Deployed!!!!!!!!!!!!!!!!")



# def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000):
#     account =account if account else get_accounts
#     link_token= get_contract("Link_Token")
#     # print(link_token)
#     tx = link_token.transfer(contract_address, amount, {"from": account})
#     # link_token_contract =interface.LinkTokenInterface(link_token)
#     # print(link_token_contract)
#     # tx = link_token_contract.transfer(contract_address, amount, {"from":account})
#     tx.wait(1)
#     return tx


def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000):
    account = get_accounts(None,'samir-account')
    # lottery = smart_lottery.deploy(get_contract("eth_usd"),
    #                            get_contract("VRFCoordinator"),
    #                            get_contract('Link_Token') ,
    #                            config["networks"][network.show_active()]["fee"],
    #                            config["networks"][network.show_active()]["keyhash"],
    #                            {"from":account},
    #                            publish_source= config["networks"][network.show_active()].get("verfiy",False)
    #                            )
    
    Link= get_contract('Link_Token')
    
    tx=Link.transfer(contract_address, amount, {"from":account})
    tx.wait(1)
    return tx

# # def main():
# # #     link_deploy()#

