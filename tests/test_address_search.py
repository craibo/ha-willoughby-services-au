from custom_components.willoughby_services.address_search import (
    AddressSearchResult,
    _parse_search_response,
)


SAMPLE_XML = """
<ListPhysicalAddressSearchResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.datacontract.org/2004/07/OpenCities.Logic.Spatial">
  <Items xmlns:d2p1="http://schemas.datacontract.org/2004/07/OpenCities.Logic.Spatial" xmlns="http://schemas.datacontract.org/2004/07/OpenCities.Logic.API">
    <d2p1:PhysicalAddressSearchResult>
      <d2p1:AddressSingleLine>2 Sunnyside Crescent, Castlecrag NSW 2068</d2p1:AddressSingleLine>
      <d2p1:Distance>0</d2p1:Distance>
      <d2p1:Id>40e960ef-85bb-4c1f-9f69-a191bf7075f7</d2p1:Id>
    </d2p1:PhysicalAddressSearchResult>
    <d2p1:PhysicalAddressSearchResult>
      <d2p1:AddressSingleLine>26 Sunnyside Crescent, Castlecrag NSW 2068</d2p1:AddressSingleLine>
      <d2p1:Distance>0</d2p1:Distance>
      <d2p1:Id>7c55cb94-955e-41d2-b930-7f7eb19ddb0f</d2p1:Id>
    </d2p1:PhysicalAddressSearchResult>
  </Items>
</ListPhysicalAddressSearchResult>
"""


def test_parse_search_response_extracts_addresses_and_ids():
    results = _parse_search_response(SAMPLE_XML)

    assert len(results) == 2

    first = results[0]
    assert isinstance(first, AddressSearchResult)
    assert first.address == "2 Sunnyside Crescent, Castlecrag NSW 2068"
    assert first.geolocation_id == "40e960ef-85bb-4c1f-9f69-a191bf7075f7"

    second = results[1]
    assert second.address == "26 Sunnyside Crescent, Castlecrag NSW 2068"
    assert second.geolocation_id == "7c55cb94-955e-41d2-b930-7f7eb19ddb0f"


def test_parse_search_response_handles_empty():
    results = _parse_search_response("<ListPhysicalAddressSearchResult></ListPhysicalAddressSearchResult>")
    assert results == []

