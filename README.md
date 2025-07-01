# cost-splitter-mcp

## Project Setup with uv

This project uses [uv](https://github.com/astral-sh/uv) for fast Python dependency management and virtual environments.

### 1. Install uv
If you don't have `uv` installed, you can install it with:

```sh
curl -Ls https://astral.sh/uv/install.sh | sh
```

Or follow the instructions on the [uv GitHub page](https://github.com/astral-sh/uv).

### 2. Create a Virtual Environment

```sh
uv venv
```

### 3. Activate the Virtual Environment

On macOS/Linux:
```sh
source .venv/bin/activate
```
On Windows:
```sh
.venv\Scripts\activate
```

### 4. Install Dependencies

```sh
uv pip install -r requirements.txt
```

### 5. Add/Update Dependencies

To add a new package:
```sh
uv pip install <package-name>
uv pip freeze > requirements.txt
```

To upgrade all packages:
```sh
uv pip install --upgrade -r requirements.txt
uv pip freeze > requirements.txt
```