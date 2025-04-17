from rest_framework import serializers
from .models import Company, BalanceHistory, User

class BalanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceHistory
        fields = ['previous_balance', 'new_balance', 'transaction_amount', 'timestamp']

class CompanySerializer(serializers.ModelSerializer):
    balance_history = serializers.SerializerMethodField()
    transaction_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, write_only=True)
    users_url = serializers.HyperlinkedIdentityField(
        view_name='company-users',
        lookup_field='pk'
    )
    num_of_user = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'total_balance', 'transaction_amount', 'balance_history', 'users_url', 'num_of_user']
    
    def get_balance_history(self, obj):
        history = obj.balance_history.all().order_by('-timestamp')
        return BalanceHistorySerializer(history, many=True).data

    def get_num_of_user(self, obj):
        return obj.users.count()

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        
        if request and request.method in ['PUT', 'PATCH']:
            # For PUT/PATCH, make total_balance read-only and enable transaction_amount
            fields['total_balance'].read_only = True
            fields['transaction_amount'].required = True
        else:
            # For POST, make transaction_amount read-only
            fields['transaction_amount'].read_only = True
        return fields
        
    def update(self, instance, validated_data):
        # Get transaction_amount from validated_data
        transaction_amount = validated_data.pop('transaction_amount', None)
        
        if transaction_amount is not None:
            # Store previous balance
            previous_balance = instance.total_balance
            # Update the total balance
            instance.total_balance += transaction_amount
            
            # Create balance history entry
            BalanceHistory.objects.create(
                company=instance,
                previous_balance=previous_balance,
                new_balance=instance.total_balance,
                transaction_amount=transaction_amount
            )
        return super().update(instance, validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'max_amount', 'company']
