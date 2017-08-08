# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity


class NewItem(scrapy.Item):
    # sql = 'INSERT INTO car_features VALUES(' \
    #       '%(id)s, %(name)s, %(baseMsrp)s, %(msrpWithTypicalOptions)s, %(mpg)s,' \
    #       '%(totalSeating)s, %(colors)s, %(safety)s, %(comfort_convenience)s,' \
    #       '%(performance)s, %(technology)s, %(fuel)s, %(engine)s, %(measurements)s, %(frontseats)s,' \
    #       '%(rearseats)s, %(drive_train)s, %(power_feature)s, %(instrumentation)s, ' \
    #       '%(suspension)s, %(in_car_entertainment)s, %(warranty)s, %(telematics)s, %(tires_and_wheels)s,' \
    #       '%(interior_options)s, %(exterior_options)s, %(packages)s,)'

    _id = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    id = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )  # mean style_id
    name = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )

    baseMsrp = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    msrpWithTypicalOptions = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    mpg = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    totalSeating = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    colors = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    safety = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    comfort_convenience = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    performance = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    technology = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    fuel = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    engine = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    measurements = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )

    frontseats = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    rearseats = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    drive_train = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    power_feature = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    instrumentation = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    suspension = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    in_car_entertainment = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    warranty = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    telematics = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    tires_and_wheels = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    interior_options = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    exterior_options = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )
    packages = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )

class CarItem(scrapy.Item):
    car_id = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity()
    )

    make_name = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    make_id = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    model_id = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    model_name = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    year = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    car_name = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )

    price = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )

    trim = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )

    submodel = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )



    base_engine = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )

    cylinder = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    drive_type = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    fuel_capacity = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    fuel_economy = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    fuel_type = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    horsepower = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    monthly_fuel_cost = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    torque = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    transmission = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    ac_with_climate_control = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    bluetooth = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    builtin_hard_drive = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    concierge_service = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    destination_download = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    destination_guidance = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    hd_radio = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    hand_free_calling = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    heatedcooled_seats = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    keyless_ignition = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    navigation = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    parking_assistance = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    power_seats = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    premium_sound_system = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    rear_seat_dvd = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    roadside_assistance = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    satellite_radio = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    seating_capacity = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    upholstery = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    ipod = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    all_season_tires = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    power_glass_sunroof = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    run_flat_tires = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    tire_size = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    wheel_tire_size = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    wheels = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    airbag_deployment_notification = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    anti_lock_brakes = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    anti_theft_system = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    child_seat_anchors = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    emergency_service = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    side_curtain_airbags = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    stabillity_control = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    stolen_vehicle_tracking_assistance = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    traction_control = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    vehicle_alarm_notification = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    average_cost_per_mile = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    true_cost_to_own = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    depreciation = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    taxes_fees = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    financing = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    fuel = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    insurance = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    maintenance = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    repairs = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    tax_credit = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )

    msrp = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    invoice = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )
    true_market_value = scrapy.Field(
        input_processor=Identity(),
        out_processor=Identity(),
    )

