from random import randint

import pytest
from sovtoken.test.helpers.helper_general import utxo_from_addr_and_seq_no

from plenum.common.exceptions import RequestRejectedException
from plenum.common.txn_util import get_seq_no


TestRunningTimeLimitSec = 500   # `test_incorrect_funds` takes time


def test_utxo_reuse(helpers, addresses, initial_mint):
    # Reproducing a test from libsovtoken
    address1, address2, address3, _, _ = addresses
    mint_seq_no = get_seq_no(initial_mint)
    inputs = [
        {"source": utxo_from_addr_and_seq_no(address1, mint_seq_no)},
    ]
    outputs = [
        {"address": address1, "amount": 100},
    ]
    request = helpers.request.transfer(inputs, outputs)
    helpers.sdk.send_and_check_request_objects([request])

    inputs = [
        {"source": utxo_from_addr_and_seq_no(address2, mint_seq_no)},
        {"source": utxo_from_addr_and_seq_no(address1, mint_seq_no)},
    ]
    outputs = [
        {"address": address3, "amount": 100},
    ]
    request = helpers.request.transfer(inputs, outputs)
    with pytest.raises(RequestRejectedException):
        helpers.sdk.send_and_check_request_objects([request])


def test_incorrect_funds(helpers, addresses, initial_mint):
    # Test doing lot of invalid (incorrect funds) txns and then finally
    # a valid txn to make sure the pool works.
    _, _, _, address4, address5 = addresses
    mint_seq_no = get_seq_no(initial_mint)
    inputs = [
        {"source": utxo_from_addr_and_seq_no(address4, mint_seq_no)},
    ]

    for i in range(200):
        if i < 100:
            amount = randint(1, 99)
        else:
            amount = randint(101, 200)

        outputs = [
            {"address": address5, "amount": amount},
        ]
        request = helpers.request.transfer(inputs, outputs)
        with pytest.raises(RequestRejectedException):
            helpers.sdk.send_and_check_request_objects([request])

    outputs = [
        {"address": address5, "amount": 100},
    ]
    request = helpers.request.transfer(inputs, outputs)
    helpers.sdk.send_and_check_request_objects([request])
