from collections import namedtuple

from marshmallow.exceptions import ValidationError

from api.queries.change import InsufficientRightsError

__all__ = ['ErrorsParser', 'ParsedError']

ParsedError = namedtuple(
    'ParsedError', ['type', 'message', 'info'], defaults={'info': None}
)


class ErrorsParser:
    @staticmethod
    def parse(exp):
        if isinstance(exp, InsufficientRightsError):
            return ErrorsParser._parse_rights(exp), 403
        if isinstance(exp, ValidationError):
            return ErrorsParser._parse_validation(exp), 422
        return ErrorsParser._parse_default(exp), 500

    @staticmethod
    def _parse_rights(exp: InsufficientRightsError):
        return ParsedError(
            type(exp).__name__,
            f'Missing "{exp.right}" right for the "{exp.target.name}"',
            info={
                'right': str(exp.right),
                'target': exp.target.id
            }
        )

    @staticmethod
    def _parse_validation(exp: ValidationError):
        return ParsedError(
            type(exp).__name__,
            f"Validation error",
            info=exp.normalized_messages()
        )

    @staticmethod
    def _parse_default(exp: Exception):
        try:
            info = dict(exp)
        except Exception:
            info = {}
        return ParsedError(
            type(exp).__name__,
            repr(exp),
            info
        )
