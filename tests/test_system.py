"""Tests for system monitoring features."""


def test_system_page_renders(client):
    """Test that system monitor page renders with 200 status."""
    response = client.get("/system")
    assert response.status_code == 200
    assert b"System Monitor" in response.data or b"System Performance" in response.data


def test_system_info_api(client):
    """Test system info API endpoint."""
    response = client.get("/api/v1/system/info")
    assert response.status_code == 200
    data = response.get_json()
    assert "timestamp" in data
    assert "system" in data
    assert "cpu" in data
    assert "memory" in data
    assert "disk" in data


def test_cpu_info_api(client):
    """Test CPU info API endpoint."""
    response = client.get("/api/v1/system/cpu")
    assert response.status_code == 200
    data = response.get_json()
    assert "physical_cores" in data
    assert "logical_cores" in data
    assert "total_usage" in data


def test_memory_info_api(client):
    """Test memory info API endpoint."""
    response = client.get("/api/v1/system/memory")
    assert response.status_code == 200
    data = response.get_json()
    assert "total" in data
    assert "used" in data
    assert "percent" in data


def test_disk_info_api(client):
    """Test disk info API endpoint."""
    response = client.get("/api/v1/system/disk")
    assert response.status_code == 200
    data = response.get_json()
    # Disk info returns a list of disk partitions
    assert isinstance(data, list) or "error" in data


def test_battery_info_api(client):
    """Test battery info API endpoint."""
    response = client.get("/api/v1/system/battery")
    assert response.status_code == 200
    data = response.get_json()
    assert "has_battery" in data
    assert "percent" in data or "error" in data


def test_network_info_api(client):
    """Test network info API endpoint."""
    response = client.get("/api/v1/system/network")
    assert response.status_code == 200
    data = response.get_json()
    # Network endpoint returns a dict with interface names as keys
    assert isinstance(data, dict) and len(data) > 0


def test_system_page_has_cpu_section(client):
    """Test system page contains CPU information."""
    response = client.get("/system")
    assert response.status_code == 200
    assert b"CPU" in response.data


def test_system_page_has_memory_section(client):
    """Test system page contains memory information."""
    response = client.get("/system")
    assert response.status_code == 200
    assert b"Memory" in response.data or b"RAM" in response.data


def test_system_page_has_disk_section(client):
    """Test system page contains disk information."""
    response = client.get("/system")
    assert response.status_code == 200
    assert b"Disk" in response.data or b"Storage" in response.data


def test_system_page_has_network_section(client):
    """Test system page contains network information."""
    response = client.get("/system")
    assert response.status_code == 200
    assert b"Network" in response.data
