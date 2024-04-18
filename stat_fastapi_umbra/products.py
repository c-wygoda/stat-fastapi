"""
Umbra Space Product Offerings
"""

from enum import Enum

from pydantic import BaseModel

from stat_fastapi.models.product import Product, Provider, ProviderRole


class SceneSizeConstraints(Enum):
    """Scene Size Contraints"""

    SCENE_5X5_KM = "5x5_KM"
    SCENE_10X10_KM = "10x10_KM"


class SpotlightConstraints(BaseModel):
    """Spotlight Constraints"""

    scene_size: SceneSizeConstraints


SPOTLIGHT_PRODUCT = Product(
    id="UMBRA:SPOTLIGHT_TASK",
    title="Umbra spotlight SAR capture",
    description="Umbra Spotlight Product",
    keywords=["sar", "radar", "umbra"],
    license="CC0-1.0",
    providers=[
        Provider(
            name="UMBRA",
            roles=[
                ProviderRole.licensor,
                ProviderRole.producer,
                ProviderRole.processor,
                ProviderRole.host,
            ],
            url="http://acme.example.com",
        )
    ],
    links=[],
    constraints=SpotlightConstraints,
)

# TODO: Add Archive product?

PRODUCTS = [
    {
        "type": "Product",
        "conformsTo": ["https://api.statspec.org/geojson#point"],
        "id": "umbra_spotlight",
        "title": "Umbra Spotlight",
        "description": "Spotlight images served by creating new Orders. Way more detail here or a link down in links to Product documentation.",
        "keywords": ["SAR", "Spotlight"],
        "license": "CC-BY-4.0",
        "providers": {
            "name": "Umbra",
            "description": "Global Omniscience",
            "roles": ["producer"],
            "url": "https://umbra.space",
        },
        "links": {
            "href": "https://docs.canopy.umbra.space",
            "rel": "documentation",
            "type": "docs",
            "title": "Canopy Documentation",
        },
        "parameters": {
            "$defs": {
                "ProductType": {
                    "enum": ["GEC", "SIDD"],
                    "title": "ProductType",
                    "type": "string",
                },
                "SceneSize": {
                    "enum": ["5x5_KM", "10x10_KM"],
                    "title": "SceneSize",
                    "type": "string",
                },
            },
            "description": "Umbra Spotlight Parameters docstring yay!",
            "properties": {
                "sceneSize": {
                    "allOf": [{"$ref": "#/$defs/SceneSize"}],
                    "default": "5x5_KM",
                    "description": "The scene size of the Spotlight collect. The first ",
                },
                "grazingAngleDegrees": {
                    "type": "number",
                    "minimum": 40,
                    "maximum": 70,
                    "description": "The minimum angle between the local tangent plane at the target location and the line of sight vector between the satellite and the target. First value is the minimum grazing angle the second is the maximum.",
                    "title": "Grazing Angle Degrees",
                },
                "satelliteIds": {
                    "description": "The satellites to consider for this Opportunity.",
                    "items": {"type": "string", "regex": "Umbra-\\d{2}"},
                    "title": "Satelliteids",
                    "type": "array",
                },
                "deliveryConfigId": {
                    "anyOf": [
                        {"format": "uuid", "type": "string"},
                        {"type": "null"},
                    ],
                    "default": None,
                    "description": "",
                    "title": "Deliveryconfigid",
                },
                "productTypes": {
                    "default": ["GEC"],
                    "description": "",
                    "items": {"$ref": "#/$defs/ProductType"},
                    "title": "Producttypes",
                    "type": "array",
                },
            },
            "required": ["satelliteIds"],
            "title": "UmbraSpotlightParameters",
            "type": "object",
        },
    },
    {
        "type": "Product",
        "conformsTo": [
            "https://api.statspec.org/geojson#polygon",
            "https://api.statspec.org/geojson#multipolygon",
        ],
        "id": "umbra_archive_catalog",
        "title": "Umbra Archive Catalog",
        "description": "Umbra SAR Images served by the Archive Catalog. Way more detail here or a link down in links to Product documentation.",
        "keywords": ["SAR", "Archive"],
        "license": "CC-BY-4.0",
        "providers": {
            "name": "Umbra",
            "description": "Global Omniscience",
            "roles": ["producer"],
            "url": "https://umbra.space",
        },
        "links": {
            "href": "https://docs.canopy.umbra.space/",
            "rel": "documentation",
            "type": "docs",
            "title": "Canopy Documentation",
        },
        "parameters": {
            "description": "Umbra Archive Catalog Parameters docstring yay!",
            "properties": {
                "sar:resolution_range": {
                    "type": "number",
                    "minimum": 0.25,
                    "maximum": 1,
                    "description": "The range resolution of the SAR Image. This is equivalent to the resolution of the ground plane projected GEC Cloud-Optimized Geotiff",
                    "title": "Range Resolution (m)",
                },
                "sar:looks_azimuth": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": 10,
                    "description": "The azimuth looks in the SAR Image. This value times the sar:resolution_range gives the azimuth resolution of the complex products.",
                    "title": "Range Resolution (m)",
                },
                "platform": {
                    "description": "The satellites to consider for this Opportunity.",
                    "title": "Platform (Satellite)",
                    "type": "string",
                    "regex": "Umbra-\\d{2}",
                },
            },
            "title": "UmbraArchiveCatalogParameters",
            "type": "object",
        },
    },
]
