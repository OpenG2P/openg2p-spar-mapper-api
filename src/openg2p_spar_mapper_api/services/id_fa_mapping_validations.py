from openg2p_g2pconnect_common_lib.mapper.schemas.resolve import (
    SingleResolveRequest,
    ResolveStatusReasonCode,
)

from openg2p_fastapi_common.service import BaseService
from openg2p_g2pconnect_common_lib.mapper.schemas import (
    LinkStatusReasonCode,
    SingleUpdateRequest,
    UpdateStatusReasonCode,
    UnlinkStatusReasonCode,
    SingleResolveRequest,
    SingleUnlinkRequest,
    SingleLinkRequest,
    ResolveStatusReasonCode,
)
from sqlalchemy import and_, select

from .exceptions import (
    LinkValidationException,
    UpdateValidationException,
    ResolveValidationException,
    UnlinkValidationException,
)
from ..models import IdFaMapping


class IdFaMappingValidations(BaseService):

    @staticmethod
    async def validate_link_request(
        connection, single_link_request: SingleLinkRequest
    ) -> None:

        # Check if the ID is null
        if not single_link_request.id:
            raise LinkValidationException(
                message="ID is null",
                validation_error_type=LinkStatusReasonCode.rjct_id_invalid,
            )

        # Check if the FA is null
        if not single_link_request.fa:
            raise LinkValidationException(
                message="FA is null",
                validation_error_type=LinkStatusReasonCode.rjct_fa_invalid,
            )

        # Check if the ID is already mapped
        result = await connection.execute(
            select(IdFaMapping).where(
                and_(
                    IdFaMapping.id_value == single_link_request.id,
                    IdFaMapping.fa_value == single_link_request.fa,
                )
            )
        )
        link_request_from_db = result.first()

        if link_request_from_db:
            raise LinkValidationException(
                message="ID and FA are already mapped",
                validation_error_type=LinkStatusReasonCode.rjct_reference_id_duplicate,
            )

        return None

    @staticmethod
    async def validate_update_request(
        connection, single_update_request: SingleUpdateRequest
    ) -> None:

        # Check if the ID is null
        if not single_update_request.id:
            raise UpdateValidationException(
                message="ID is null",
                validation_error_type=UpdateStatusReasonCode.rjct_id_invalid,
            )

        # Check if the FA is null
        if not single_update_request.fa:
            raise UpdateValidationException(
                message="FA is null",
                validation_error_type=UpdateStatusReasonCode.rjct_fa_invalid,
            )

        # Check if the ID is already mapped
        result = await connection.execute(
            select(IdFaMapping).where(
                and_(
                    IdFaMapping.id_value == single_update_request.id,
                    IdFaMapping.fa_value == single_update_request.fa,
                )
            )
        )
        link_request_from_db = result.first()

        if link_request_from_db is None:
            raise UpdateValidationException(
                message="ID doesnt exist please link first",
                validation_error_type=UpdateStatusReasonCode.rjct_reference_id_duplicate,
            )

        return None

    @staticmethod
    async def validate_resolve_request(
        connection, single_resolve_request: SingleResolveRequest
    ) -> None:

        # Check if the ID is null
        if not single_resolve_request.id:
            raise ResolveValidationException(
                message="ID is null",
                validation_error_type=ResolveStatusReasonCode.rjct_id_invalid,
            )

        # Check if the FA is null
        if not single_resolve_request.fa:
            raise ResolveValidationException(
                message="FA is null",
                validation_error_type=ResolveStatusReasonCode.rjct_fa_invalid,
            )

        # Check if the ID is already mapped
        result = await connection.execute(
            select(IdFaMapping).where(
                and_(
                    IdFaMapping.id_value == single_resolve_request.id,
                    IdFaMapping.fa_value == single_resolve_request.fa,
                )
            )
        )
        link_request_from_db = result.first()

        if link_request_from_db:
            raise ResolveValidationException(
                message="ID doesnt exist please link first",
                validation_error_type=ResolveStatusReasonCode.rjct_reference_id_duplicate,
            )
        return None

    @staticmethod
    async def validate_unlink_request(
        connection, single_unlink_request: SingleUnlinkRequest
    ) -> None:

        if not single_unlink_request.id:
            raise UnlinkValidationException(
                message="ID is null",
                validation_error_type=UnlinkValidationException.rjct_id_invalid,
            )

        if not single_unlink_request.fa:
            raise UnlinkValidationException(
                message="FA is null",
                validation_error_type=UnlinkValidationException.rjct_fa_invalid,
            )
        result = await connection.execute(
            select(IdFaMapping).where(
                and_(
                    IdFaMapping.id_value == single_unlink_request.id,
                    IdFaMapping.fa_value == single_unlink_request.fa,
                )
            )
        )
        link_request_from_db = result.first()

        if link_request_from_db is None:
            raise UnlinkValidationException(
                message="ID doesnt exist please link first",
                validation_error_type=UnlinkStatusReasonCode.rjct_reference_id_duplicate,
            )

        return None
