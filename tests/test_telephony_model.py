from src.ui.models.network import TelephonyModel


def test_telephony_model_from_dict_complete():
    data = {
        "deviceinfo": {
            "network_operator_name": "MyCarrier",
            "phone_type": "GSM"
        },
        "signalstrength": {"dbm": -70},
        "cellinfo": [{"type": "LTE"}]
    }
    model = TelephonyModel.from_dict(data)
    # The actual code doesn't call .upper() on carrier
    assert model.carrier == "MyCarrier"
    assert model.cell_type == "LTE"
    assert model.signal_dbm == "-70 dBm"

def test_telephony_model_from_dict_missing_data():
    data = {"deviceinfo": {"error": "API Access Denied"}}
    model = TelephonyModel.from_dict(data)
    # The actual code uses 'Access Denied' when "error" is present in deviceinfo
    assert model.carrier == "Access Denied"
    assert model.cell_type == "N/A"
    assert model.signal_dbm == "N/A"

def test_telephony_model_from_dict_normalization():
    # Test phone_type fallback
    data = {
        "deviceinfo": {"phone_type": "CDMA"},
        "cellinfo": []
    }
    model = TelephonyModel.from_dict(data)
    assert model.cell_type == "CDMA"
