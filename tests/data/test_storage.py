import pytest
from src.data.storage import YAMLStorage


@pytest.fixture
def yaml_storage():
    return YAMLStorage()


def test_save_and_load_simple(yaml_storage, tmp_path):
    """Test basic save and load functionality."""
    file_path = tmp_path / "test.yaml"
    data = {"name": "test", "value": 123}

    yaml_storage.save(data, file_path)
    assert file_path.exists()

    loaded_data = yaml_storage.load(file_path)
    assert loaded_data == data


def test_comment_preservation(yaml_storage, tmp_path):
    """Test that comments are preserved during round-trip."""
    file_path = tmp_path / "comments.yaml"

    # Create initial file with comments
    initial_content = """
# This is a root comment
key: value  # This is an inline comment
list:
  - item1
  # Comment in list
  - item2
"""
    file_path.write_text(initial_content.strip(), encoding="utf-8")

    # Load the data
    data = yaml_storage.load(file_path)

    # Modify data (add a key)
    data["new_key"] = "new_value"

    # Save back
    yaml_storage.save(data, file_path)

    # Read raw content to check comments
    content = file_path.read_text(encoding="utf-8")

    assert "# This is a root comment" in content
    assert "# This is an inline comment" in content
    assert "# Comment in list" in content
    assert "new_key: new_value" in content


def test_file_not_found(yaml_storage, tmp_path):
    """Test error handling for non-existent files."""
    with pytest.raises(FileNotFoundError):
        yaml_storage.load(tmp_path / "non_existent.yaml")


def test_invalid_yaml(yaml_storage, tmp_path):
    """Test error handling for invalid YAML content."""
    file_path = tmp_path / "invalid.yaml"
    file_path.write_text("key: value: invalid", encoding="utf-8")

    from ruamel.yaml import YAMLError

    with pytest.raises(YAMLError):
        yaml_storage.load(file_path)
