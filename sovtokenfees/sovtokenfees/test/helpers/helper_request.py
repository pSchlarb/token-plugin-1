import json

from indy.payment import add_request_fees, build_set_txn_fees_req, build_get_txn_fees_req

from plenum.common.request import Request
from sovtoken.test.helpers import HelperRequest
from sovtokenfees.test.constants import txn_type_to_alias
from sovtokenfees.test.helpers.abstract_helper_request import AbstractHelperRequest
from plenum.common.constants import TXN_TYPE, ALIAS
from sovtokenfees.constants import SET_FEES, FEES, GET_FEES, GET_FEE
from sovtoken.constants import AMOUNT, ADDRESS

from stp_core.common.log import getlogger

logger = getlogger()


class HelperRequest(AbstractHelperRequest, HelperRequest):
    """
    Extends the sovtoken HelperRequest with fee related requests.

    # Methods
    - set_fees
    - get_fees
    - add_fees
    - add_fees_specific
    - find_utxos_can_pay
    - fees_signatures
    """

    def set_fees(self, fees):
        """ Build a request to set the fees. """

        request = build_set_txn_fees_req(self._client_wallet_handle, self._wallet._trustees[0], 'sov', json.dumps(fees))
        request = self._looper.loop.run_until_complete(request)
        request = self._wallet.sign_request_trustees(request, number_signers=3)
        request = json.loads(request)
        sigs = request["signatures"]
        request = self._sdk.sdk_json_to_request_object(request)
        setattr(request, "signatures", sigs)
        return request

    def get_fees(self):
        """ Build a request to get the fees. """
        request = build_get_txn_fees_req(self._client_wallet_handle, None, 'sov')
        request = self._looper.loop.run_until_complete(request)
        request = self._sdk.sdk_json_to_request_object(json.loads(request))
        return request

    def get_fee(self, alias):
        """ Build a request to get the fees. """
        payload = {
            TXN_TYPE: GET_FEE,
            ALIAS: alias
        }

        request = self._create_request(payload, identifier=self._client_did)
        return request

    def nym_new(self, identifier=None, sdk_wallet=None):
        return self._sdk.sdk_build_nym(identifier=identifier, sdk_wallet=sdk_wallet)

    def attrib(self, identifier=None, sdk_wallet=None):
        return self._sdk.sdk_build_attrib(identifier=identifier, sdk_wallet=sdk_wallet)

    def schema_new(self, identifier=None, sdk_wallet=None):
        return self._sdk.sdk_build_schema(identifier=identifier, sdk_wallet=sdk_wallet)

    def claim_def(self, schema_json, identifier=None, sdk_wallet=None):
        return self._sdk.sdk_build_claim_def(schema_json, identifier=identifier, sdk_wallet=sdk_wallet)

    def revoc_reg_def(self, claim_def_id, identifier=None, sdk_wallet=None):
        return self._sdk.sdk_build_revoc_reg_def(claim_def_id, identifier=identifier, sdk_wallet=sdk_wallet)

    def revoc_reg_entry(self, claim_def_id, identifier=None, sdk_wallet=None):
        return self._sdk.sdk_build_revoc_reg_entry(claim_def_id, identifier=identifier, sdk_wallet=sdk_wallet)

    def add_fees_to_req(self, request, inputs, outputs):
        request_with_fees_future = add_request_fees(self._client_wallet_handle, None, json.dumps(request.as_dict),
                                                    json.dumps(inputs), json.dumps(outputs), None)
        return self._looper.loop.run_until_complete(request_with_fees_future)

    def get_txn(self, ledger_id, seq_no):
        req = self._sdk.sdk_build_get_txn(ledger_id, seq_no)
        req = Request(**json.loads(req))
        return req
