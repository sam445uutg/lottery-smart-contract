// SPDX-License-Identifier:MIT

pragma solidity <=0.8.0;

import "node_modules/@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "node_modules/@openzeppelin/contracts/access/Ownable.sol";
import "node_modules/@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract smart_lottery is VRFConsumerBase, Ownable{
    // golbal variable
    address payable[] public players;
    uint256 public USD_amt;
    address payable public winner;
    AggregatorV3Interface internal ethusd_preice_feed;
    uint256 public randomness;
    enum LOTTERY_STATE {
        CLOSED,
        OPENED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256  public fee;
    bytes32 public keyHash;



    constructor (address _pricefeed, address _vrfCoordinator ,address _link,uint256 _fee,bytes32 _keyHash) 
    public VRFConsumerBase( _vrfCoordinator, _link){
        USD_amt= 5*(10**18);
        ethusd_preice_feed = AggregatorV3Interface(_pricefeed);
        lottery_state =LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }
    function enter() public payable{
        //require(amt_usd );
        require(lottery_state == LOTTERY_STATE.OPENED);
        require(msg.value > getenterancefee(), "NOT ENOUGH ETH !!! NEXT TIME TRY>>>");
        players.push(payable(msg.sender));
    } 
    function getenterancefee() public view returns (uint256){
        (,int256 price,,,) = ethusd_preice_feed.latestRoundData();
        uint256 adjuest_price = uint256(price)* 10**10;
        uint256 cost_to_enter =((USD_amt*10**18) / adjuest_price);
        return cost_to_enter;
    }
    function start_lottery()public onlyOwner{
        require(lottery_state == LOTTERY_STATE.CLOSED,"Can't start  a new lottery yet");
        lottery_state = LOTTERY_STATE.OPENED;
    }
    function end_lottery() public onlyOwner{
        // uint(
        //     keccak256(
        //         abi.encodePacked(
        //             //nonce,
        //             msg.sender,
        //             block.difficulty,
        //             block.timestamp
        //         )
        //     )
        // )% players.length;
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
    }
    function fulfillRandomness (bytes32 _requestId, uint256 _randomness) internal override{
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER);
        require(randomness>0,"random-not-found");
        uint256 indexofwinner = randomness% players.length;
        winner = players[indexofwinner];
        winner.transfer(address(this).balance);
        //reset
        players = new address payable[](0);
        lottery_state =LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}