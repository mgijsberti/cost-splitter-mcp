# cost-splitter-mcp

**Cost Splitter MCP Service**

This application provides a service to split shared expenses among a group of people. Users can input how much each person paid, and the service calculates the minimal set of transactions required to equalize costs so that everyone ends up having paid the same amount. The service is implemented as a FastMCP tool (`equalize_costs`) and can be accessed programmatically or tested via integration and unit tests.

## How to configure as local MCP server for Claude  Desktop

Add to Claude Desktop configuration file:

```  "cost-splitter":{
      "command" : "uv",
      "args" : [
         "--directory",
        "/Users/mgijsberti/Documents/Projects/cost-splitter-mcp",
        "run",
        "main.py"
      ]
    } 
```

## Try in the Claude Desktop the following prompt:

```
Hi Alice has paid 100 euros, Bob has paid 60 euros, Charlie 40 euros and David has paid 20 euros. How would you equalize the costs ?

``` 

The expected output is: 

```Here's how to equalize the costs:
Total paid: 220 euros
Equal share per person: 55 euros each
Transfers needed:

David pays Alice: 35 euros
Charlie pays Alice: 10 euros
Charlie pays Bob: 5 euros

Final result:

Alice: 100 - 35 - 10 = 55 euros
Bob: 60 - 5 = 55 euros
Charlie: 40 + 10 + 5 = 55 euros
David: 20 + 35 = 55 euros

Everyone ends up having paid exactly 55 euros, which is their fair share of the total 220 euros.
```


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

### 6. Run tests 

in terminal execute:
```sh
    ./run_all.tests.sh
```
