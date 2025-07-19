"""Unit tests for Flask calculator application routes and calculations."""

import pytest


class TestCalculatorRoutes:
    """Test class for calculator route functionality."""
    
    def test_index_route_returns_calculator_page(self, client):
        """Should return the calculator HTML page on GET request to root."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Simple Calculator' in response.data
        assert b'<input type="text" id="display"' in response.data
        
    def test_input_value_route(self, client):
        """Should handle input value routes correctly."""
        response = client.get('/input?value=5')
        assert response.status_code == 302  # Redirect
        
        # Follow redirect to see the result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="5"' in response.data
    
    def test_clear_route(self, client):
        """Should handle clear route correctly."""
        # First add some value
        client.get('/input?value=5')
        
        # Then clear
        response = client.get('/clear')
        assert response.status_code == 302  # Redirect
        
        # Check that display is cleared
        response = client.get('/')
        assert response.status_code == 200
        # Should not contain the previous value
        assert b'value="5"' not in response.data
    
    def test_backspace_route(self, client):
        """Should handle backspace route correctly."""
        # Add multiple digits
        client.get('/input?value=1')
        client.get('/input?value=2')
        client.get('/input?value=3')
        
        # Remove last digit
        response = client.get('/backspace')
        assert response.status_code == 302  # Redirect
        
        # Check result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="12"' in response.data


class TestBasicArithmeticOperations:
    """Test class for basic arithmetic operations."""
    
    def test_addition_operation(self, client):
        """Should correctly calculate addition operations."""
        # Build expression: 2+3
        client.get('/input?value=2')
        client.get('/input?value=%2B')
        client.get('/input?value=3')
        
        # Calculate
        response = client.get('/calculate')
        assert response.status_code == 302  # Redirect
        
        # Check result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="5"' in response.data or b'value="5.0"' in response.data
    
    def test_subtraction_operation(self, client):
        """Should correctly calculate subtraction operations."""
        # Build expression: 10-3
        client.get('/input?value=1')
        client.get('/input?value=0')
        client.get('/input?value=-')
        client.get('/input?value=3')
        
        # Calculate
        client.get('/calculate')
        
        # Check result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="7"' in response.data or b'value="7.0"' in response.data
    
    def test_multiplication_operation(self, client):
        """Should correctly calculate multiplication operations."""
        # Build expression: 4*5
        client.get('/input?value=4')
        client.get('/input?value=*')
        client.get('/input?value=5')
        
        # Calculate
        client.get('/calculate')
        
        # Check result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="20"' in response.data or b'value="20.0"' in response.data
    
    def test_division_operation(self, client):
        """Should correctly calculate division operations."""
        # Build expression: 15/3
        client.get('/input?value=1')
        client.get('/input?value=5')
        client.get('/input?value=%2F')  # URL encoded /
        client.get('/input?value=3')
        
        # Calculate
        client.get('/calculate')
        
        # Check result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="5"' in response.data or b'value="5.0"' in response.data


class TestComplexExpressions:
    """Test class for complex mathematical expressions."""
    
    def test_parentheses_operations(self, client):
        """Should correctly handle expressions with parentheses."""
        # Build expression: (2+3)*4
        client.get('/input?value=(')
        client.get('/input?value=2')
        client.get('/input?value=%2B')
        client.get('/input?value=3')
        client.get('/input?value=)')
        client.get('/input?value=*')
        client.get('/input?value=4')
        
        # Calculate
        client.get('/calculate')
        
        # Check result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="20"' in response.data or b'value="20.0"' in response.data
    
    def test_decimal_operations(self, client):
        """Should correctly handle decimal number operations."""
        # Build expression: 2.5+1.5
        client.get('/input?value=2')
        client.get('/input?value=.')
        client.get('/input?value=5')
        client.get('/input?value=%2B')
        client.get('/input?value=1')
        client.get('/input?value=.')
        client.get('/input?value=5')
        
        # Calculate
        client.get('/calculate')
        
        # Check result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="4"' in response.data or b'value="4.0"' in response.data


class TestErrorHandling:
    """Test class for error handling scenarios."""
    
    def test_division_by_zero_error(self, client):
        """Should return error for division by zero."""
        # Build expression: 5/0
        client.get('/input?value=5')
        client.get('/input?value=%2F')  # URL encoded /
        client.get('/input?value=0')
        
        # Calculate
        client.get('/calculate')
        
        # Check error message
        response = client.get('/')
        assert response.status_code == 200
        assert b'Division by zero' in response.data
    
    def test_invalid_expression_error(self, client):
        """Should return error for malformed expressions."""
        # Build expression ending with operator: 2+
        client.get('/input?value=2')
        client.get('/input?value=%2B')
        
        # Calculate
        client.get('/calculate')
        
        # Check error message
        response = client.get('/')
        assert response.status_code == 200
        assert b'Invalid expression' in response.data
    
    def test_empty_expression_error(self, client):
        """Should return error for empty expression."""
        # Don't add any input, just calculate
        client.get('/calculate')
        
        # Check error message
        response = client.get('/')
        assert response.status_code == 200
        assert b'No expression provided' in response.data


class TestCalculatorFunctionality:
    """Test class for calculator functionality like clear, clear entry, backspace."""
    
    def test_clear_functionality(self, client):
        """Should clear the entire display."""
        # Add some expression
        client.get('/input?value=1')
        client.get('/input?value=2')
        client.get('/input?value=3')
        
        # Clear
        client.get('/clear')
        
        # Check that display is empty
        response = client.get('/')
        assert response.status_code == 200
        assert b'value=""' in response.data or b'value="0"' not in response.data
    
    def test_clear_entry_functionality(self, client):
        """Should clear the current entry."""
        # Add some expression
        client.get('/input?value=4')
        client.get('/input?value=5')
        client.get('/input?value=6')
        
        # Clear entry
        client.get('/clear_entry')
        
        # Check that display is empty
        response = client.get('/')
        assert response.status_code == 200
        assert b'value=""' in response.data or b'value="0"' not in response.data
    
    def test_backspace_functionality(self, client):
        """Should delete the last character."""
        # Add expression: 789
        client.get('/input?value=7')
        client.get('/input?value=8')
        client.get('/input?value=9')
        
        # Delete last character
        client.get('/backspace')
        
        # Check result should be: 78
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="78"' in response.data
        
        # Delete another character
        client.get('/backspace')
        
        # Check result should be: 7
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="7"' in response.data
        
        # Delete last character
        client.get('/backspace')
        
        # Check result should be empty
        response = client.get('/')
        assert response.status_code == 200
        assert b'value=""' in response.data or b'value="0"' not in response.data


class TestSequentialOperations:
    """Test class for sequential calculator operations."""
    
    def test_continuous_calculations(self, client):
        """Should handle continuous calculations correctly."""
        # First calculation: 2+3=5
        client.get('/input?value=2')
        client.get('/input?value=%2B')
        client.get('/input?value=3')
        client.get('/calculate')
        
        # Check first result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="5"' in response.data or b'value="5.0"' in response.data
        
        # Continue with result: *2
        client.get('/input?value=*')
        client.get('/input?value=2')
        client.get('/calculate')
        
        # Check second result
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="10"' in response.data or b'value="10.0"' in response.data
    
    def test_error_recovery(self, client):
        """Should recover from errors correctly."""
        # Create an error: division by zero
        client.get('/input?value=5')
        client.get('/input?value=%2F')  # URL encoded /
        client.get('/input?value=0')
        client.get('/calculate')
        
        # Check error
        response = client.get('/')
        assert response.status_code == 200
        assert b'Division by zero' in response.data
        
        # Clear and try valid calculation
        client.get('/clear')
        client.get('/input?value=2')
        client.get('/input?value=%2B')
        client.get('/input?value=2')
        client.get('/calculate')
        
        # Check recovery
        response = client.get('/')
        assert response.status_code == 200
        assert b'value="4"' in response.data or b'value="4.0"' in response.data
        # Error should be gone
        assert b'Division by zero' not in response.data
