function getData(path) {
    const fs = require("fs")
    const text = fs.readFileSync(path).toString("utf-8")
    return text.split("\n")
};

let CARD2NUM = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
            }

function parseInput(row) {
    const [cardsString, bidString] = row.split(" ")
    
    const cards = [...cardsString].map(card => CARD2NUM[card])
    const bid = parseInt(bidString)

    return [cards, bid]
}


class Hand {
    constructor(cards, bid) {
        this.cards = cards
        this.cardsDict = Hand.#cardsToDict(cards)
        this.score = Hand.#cardsDictToScore(this.cardsDict)
        this.bid = bid
    }

    static #cardsToDict(cards) {
        let countDict = {};
        for (let i=0; i < cards.length; i++) {
            countDict[cards[i]] = (countDict[cards[i]] || 0 ) +1;
        }

        let cardsDict = {};
        for (const [value, numberOf] of Object.entries(countDict)) {
            if (numberOf in cardsDict) {
                cardsDict[numberOf].push(value)
            } else {
                cardsDict[numberOf] = [value]
            }
        }

        return cardsDict
    }

    static #cardsDictToScore(cardsDict) {
        if (5 in cardsDict) {
            return 7    
        }
        
        if (4 in cardsDict) {
            return 6
        }

        if (3 in cardsDict && 2 in cardsDict) {
            return 5
        }

        if (3 in cardsDict) {
            return 4
        }

        if (2 in cardsDict && cardsDict[2].length === 2) {
            return 3
        }

        if (2 in cardsDict) {
            return 2
        }

        return 1
    }

    #eq(other) {
        if (this.score !== other.score) {
            return false
        }

        for (let i = 0; i < this.cards.length; i++) {
            if (this.cards[i] !== other.cards[i]) {
                return false
            }
        }

        return true
    }

    #gt(other) {
        if (this.score > other.score) {
            return true
        } else if (this.score < other.score) {
            return false
        }

        for (let i = 0; i < this.cards.length; i++) {
            if (this.cards[i] > other.cards[i]) {
                return true
            } else if (this.cards[i] < other.cards[i]) {
                return false
            }
        }

        return false
    }

    static compare(first, second) {
        if (first.#eq(second)) {
            return 0
        } else if (first.#gt(second)) {
            return 1
        } else {
            return -1
        }
    }
}


function partOne() {
    const rows = getData("./7/input.txt")
    const cardBids = rows.map(parseInput)
    const hands = cardBids.map(cardBid => new Hand(...cardBid))
    
    const sortedHands = hands.sort((a, b) => Hand.compare(a, b))
    const score = sortedHands.map((hand, idx) => hand.bid * (idx+1)).reduce((partialSum, a) => partialSum + a, 0)

    // for (hand of sortedHands) {
    //     console.log(hand.cards)
    // }
    console.log(score)
}


class JokerHand extends Hand {
    constructor(cards, bid) {
        const jokerIndex = cards.indexOf(1)
        if (jokerIndex >= 0) {
            let possibleHands = []
            for (let value = 2; value < 15; value++) {
                let newCards = [...cards]
                newCards[jokerIndex] = value
                possibleHands.push(new JokerHand(newCards, bid)) 
            }

            possibleHands = possibleHands.flat()
            if (possibleHands.length > 13) {
                console.log(possibleHands)
            }

            const sortedPossibleHands = possibleHands.sort((a, b) => Hand.compare(a, b))
            const bestHand = sortedPossibleHands.slice(-1)[0]
            super(cards, bid)
            this.score = bestHand.score
        
        } else {
            super(cards, bid)            
        }
    }
}


function partTwo() {
    CARD2NUM["J"] = 1
    const rows = getData("./7/input.txt")
    const cardBids = rows.map(parseInput)
    const hands = cardBids.map(cardBid => new JokerHand(...cardBid))
    
    const sortedHands = hands.sort((a, b) => Hand.compare(a, b))
    const score = sortedHands.map((hand, idx) => hand.bid * (idx+1)).reduce((partialSum, a) => partialSum + a, 0)

    // for (hand of sortedHands) {
    //     console.log(hand.cards)
    // }
    console.log(score)

}


// partOne()
partTwo()
