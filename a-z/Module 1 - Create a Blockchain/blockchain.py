import datetime
import hashlib
import json

from flask import Flask, jsonify, make_response

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        block = {
            'proof': proof,
            'previous_hash': previous_hash,
            'timestamp': str(datetime.datetime.now()),
            'index': len(self.chain) + 1
        }

        self.chain.append(block)

        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        proof = 1
        CHECK_PROOF = False

        while(not CHECK_PROOF):
            hashed_proof = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hashed_proof[:4] == '0000':
                CHECK_PROOF = True
            else:
                proof += 1
        
        return proof
    
    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def is_chain_valid(self, chain):
        previous_block_index = 0
        current_block_index = 1

        while(current_block_index < len(chain)):
            previous_block = chain[previous_block_index]
            current_block = chain[current_block_index]

            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            
            hashed_proof = hashlib.sha256(str(current_block['proof']**2 - previous_block['proof']**2).encode()).hexdigest()

            if hashed_proof[:4] != '0000':
                return False
            
            previous_block_index = current_block_index
            current_block_index += 1
        
        return True

            

        

# # Flask web app
app = Flask(__name__)

# blockchain instance

blockchain = Blockchain()


@app.route('/mine_block')
def mine_block():
    previous_block = blockchain.get_previous_block()
    new_proof = blockchain.proof_of_work(previous_block['proof'])
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(new_proof, previous_hash)

    return make_response(block, 200)

@app.route('/get_chain')
def get_chain():
    

    return make_response(jsonify({
        'chain': blockchain.chain
    }), 200)

@app.route('/is_valid')
def is_valid():
    

    return make_response(jsonify({
        'is_valid': blockchain.is_chain_valid(blockchain.chain)
    }), 200)

app.run(host='0.0.0.0', port=3000, debug=True)
