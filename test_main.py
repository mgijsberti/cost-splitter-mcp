"""Unit tests for the split_costs function in the cost-splitter MCP service."""
# pylint: disable=trailing-whitespace
import pytest
from main import split_costs, Person, Transaction


class TestSplitCosts:
    """Test cases for the split_costs function."""
    def test_empty_list(self):
        """Test with empty list of people"""
        result = split_costs([])
        assert not result

    def test_single_person(self):
        """Test with single person"""
        people = [Person(name="Alice", paid=100.0)]
        result = split_costs(people)
        assert not result

    def test_two_people_equal_payment(self):
        """Test with two people who paid equal amounts"""
        people = [
            Person(name="Alice", paid=50.0),
            Person(name="Bob", paid=50.0)
        ]
        result = split_costs(people)
        assert not result

    def test_two_people_unequal_payment(self):
        """Test with two people who paid different amounts"""
        people = [
            Person(name="Alice", paid=60.0),
            Person(name="Bob", paid=40.0)
        ]
        result = split_costs(people)
        assert result == [Transaction(**{"from": "Bob", "to": "Alice", "amount": 10.0})]

    def test_three_people_simple_split(self):
        """Test with three people - simple case"""
        people = [
            Person(name="Alice", paid=100.0),
            Person(name="Bob", paid=50.0),
            Person(name="Charlie", paid=50.0)
        ]
        result = split_costs(people)
        assert len(result) == 2
        assert result[0].amount == pytest.approx(16.67, abs=0.02)
        assert result[1].amount == pytest.approx(16.67, abs=0.02)

    def test_three_people_complex_split(self):
        """Test with three people - more complex case"""
        people = [
            Person(name="Alice", paid=120.0),
            Person(name="Bob", paid=80.0),
            Person(name="Charlie", paid=40.0)
        ]
        result = split_costs(people)
        expected = [
            Transaction(**{"from": "Charlie", "to": "Alice", "amount": 40.0})
        ]
        assert result == expected

    def test_four_people_split(self):
        """Test with four people"""
        people = [
            Person(name="Alice", paid=100.0),
            Person(name="Bob", paid=60.0),
            Person(name="Charlie", paid=40.0),
            Person(name="David", paid=20.0)
        ]
        result = split_costs(people)
        # Total: 220, Average: 55
        # Alice: +45, Bob: +5, Charlie: -15, David: -35
        # Check that the net effect of transactions brings everyone to the average
        net_received = {p.name: 0.0 for p in people}
        for t in result:
            net_received[t.from_person] -= t.amount
            net_received[t.to] += t.amount       
        avg = sum(p.paid for p in people) / len(people)
        for p in people:
            # Net payment = original paid - net received
            # This should equal the average amount each person should have paid
            net_payment = p.paid - net_received[p.name]
            assert abs(net_payment - avg) < 0.01, (
                f"{p.name} net payment {net_payment} does not equal average {avg}")

    def test_decimal_precision(self):
        """Test that amounts are rounded to 2 decimal places"""
        people = [
            Person(name="Alice", paid=33.33),
            Person(name="Bob", paid=33.33),
            Person(name="Charlie", paid=33.34)
        ]
        result = split_costs(people)
        assert not result

    def test_large_amounts(self):
        """Test with large amounts"""
        people = [
            Person(name="Alice", paid=1000.0),
            Person(name="Bob", paid=500.0),
            Person(name="Charlie", paid=1500.0)
        ]
        result = split_costs(people)
        expected = [Transaction(**{"from": "Bob", "to": "Charlie", "amount": 500.0})]
        assert result == expected

    def test_negative_amounts(self):
        """Test that negative amounts are handled correctly"""
        people = [
            Person(name="Alice", paid=-50.0),
            Person(name="Bob", paid=150.0)
        ]
        result = split_costs(people)
        expected = [Transaction(**{"from": "Alice", "to": "Bob", "amount": 100.0})]
        assert result == expected

    def test_transaction_attributes(self):
        """Test that Transaction objects have correct attributes"""
        people = [
            Person(name="Alice", paid=60.0),
            Person(name="Bob", paid=40.0)
        ]
        result = split_costs(people)
        assert len(result) == 1
        transaction = result[0]
        assert transaction.from_person == "Bob"
        assert transaction.to == "Alice"
        assert transaction.amount == 10.0  # pylint: disable=trailing-whitespace

# pylint: disable=missing-final-newline
        