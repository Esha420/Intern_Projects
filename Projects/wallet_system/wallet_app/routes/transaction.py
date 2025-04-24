from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.transaction import TransactionService

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    try:
        transaction = TransactionService.create_transaction(
            user_id=current_user['id'],
            amount=data['amount'],
            transaction_type='transfer',
            recipient_id=data['recipient_id']
        )
        return jsonify({
            'message': 'Transfer successful',
            'transaction': {
                'reference': transaction.reference,
                'amount': transaction.amount,
                'fee': transaction.fee,
                'status': transaction.status
            }
        }), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 400