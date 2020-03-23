from deepmerge import always_merger
from flask import jsonify, request, session
from flask_login import current_user

from api.system import HierachyManager
from utils import Singleton

from .script_manager import Context, ScriptManager

__all__ = ['ServerScriptExecutor']


# TODO not thread-safe?
class ServerScriptExecutor(metaclass=Singleton):
    def __init__(self):
        self._mgr = ScriptManager()
        self._hmgr = HierachyManager()
        self._mgr.set_session(session)
        self._reset()

    def _reset(self):
        self.return_ = None
        self.append_ = {}

    def process_logic(self, activation, elem, request_info=None):
        self._reset()
        if elem.triggerList is None:
            return True
        return self._process(
            activation, elem, request_info,
            elem.triggerList.get_scripts(activation)
        )

    def process_global(self, activation, request_info=None):
        self._reset()
        return self._process(
            activation, None, request_info,
            self._hmgr.h.triggers.get_scripts(activation)
        )

    def process_call(self, id, activation, request_info=None):
        self._reset()
        return self._process(activation, None, request_info, [id])

    def _process(self, activation, elem, request_info, script_ids):
        if len(script_ids) == 0:
            return True

        ctx = Context(
            activation=activation,
            user=current_user,
            elem=elem,
            request=request,
            request_info=request_info
        )
        if len(script_ids) == 1:
            return self._dispatch_one(ctx, script_ids[0])
        return self._dispatch_many(ctx, script_ids)

    def _dispatch_one(self, ctx: Context, id):
        ret = self._mgr.execute(id, ctx)
        if ret.abort:
            self.return_ = (
                jsonify(
                    {
                        "ok": False,
                        "message": ret.abort_msg,
                        "business_logic": ret.append_request
                    }
                ), ret.abort
            )
            return False
        self.append_ = {"business_logic": ret.append_request}
        return True

    def _dispatch_many(self, ctx: Context, ids):
        ret = {}
        status = True
        for id in ids:
            status = status and self._dispatch_one(ctx, id)
            ret = always_merger.merge(ret, self.append_)
        self.append_ = ret
        return status
