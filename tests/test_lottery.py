#0.0048987429825507
#48987429825507

from eth_account import Account
from brownie import accounts, smart_lottery, config, network
from web3 import Web3

def test_get_enterance():
    account =accounts[0]
    lottery= smart_lottery.deploy(config["networks"][network.show_active()]["eth_usd"],{"from":account})

    assert lottery.getenterancefee()  >Web3.toWei(0.003,"ether")
    assert lottery.getenterancefee() < Web3.toWei(0.005,"ether")
    #assert lottery.getenterancefee() == Web3.toWei(0.0048987429825, "ether")
