Naming guides for Montana Swiss Watches Website API.

# **Naming Conventions for Montana Swiss Watches Website API**

This document defines the naming conventions to be followed across the Montana Swiss Watches Website API. Consistent naming ensures clarity, maintainability, and efficiency in both individual and team development.

---

## **Naming Keywords**

The following abbreviations are used as keywords to represent CRUD (Create, Read, Update, Delete) operations in resource names:


| **Keyword** | **Operation**     | **Description**                            |
| ----------- | ----------------- | ------------------------------------------ |
| `Cr`        | Create            | Represents creating a new resource.        |
| `Up`        | Update            | Represents updating an existing resource.  |
| `De`        | Delete            | Represents deleting a resource.            |
| `Re`        | Read (Get/Select) | Represents fetching or reading a resource. |

---

## **Schema Naming Guide**

Schemas follow the format:
**`<Resource><Operation>[Suffix]Schema`**

### **Components**

1. **`Resource`**: A short abbreviation representing the entity being acted upon (e.g., `Wa` for Watch, `Us` for User).
2. **`Operation`**: A two-letter abbreviation for the CRUD operation (`Cr`, `Up`, `De`, `Re`).
3. **`Suffix`** *(optional)*: Additional context for the schema:
   - `ParamSchema`: Used for input parameters.
   - `ResponseSchema`: Used for API responses.
   - `DetailSchema`: Used for detailed or nested object representations.
   - `RequestSchema`: Used for body of the request in methods where body can be used

### **Examples**


| **Resource** | **Operation** | **Suffix**   | **Schema Name**    | **Description**                          |
| ------------ | ------------- | ------------ | ------------------ | ---------------------------------------- |
| `Wa`         | `Cr`          | None         | `WaCrSchema`       | Schema for creating a watch.             |
| `Wa`         | `Up`          | `PaSchema`   | `WaUpParamsSchema` | Schema for input data to update a watch. |
| `Wa`         | `Re`          | `RespSchema` | `WaReRespSchema`   | Schema for watch data in API responses.  |
| `Us`         | `Cr`          | None         | `UsCrSchema`       | Schema for creating a user.              |
| `Us`         | `Re`          | `RespSchema` | `UsReRespSchema`   | Schema for user data in API responses.   |

---

## **Model Naming Guide**

Models should follow these conventions:

- **Plural Names**: Models should be named in plural form to represent collections of resources.
- **Model Suffix**: All models should end with the `Model` suffix.

### **Examples**


| **Entity** | **Model Name**     |
| ---------- | ------------------ |
| Watch      | `WatchesModel`     |
| User       | `UsersModel`       |
| Collection | `CollectionsModel` |

---

## **API Endpoint Naming**

- **Format**: Use **kebab-case** for API endpoints.
- **Structure**: `/api/<resource>/<version>/<action>/`
- Examples:
  - `/api/watches/v1/create/` for creating a new watch.
  - `/api/users/v1/get/` for retrieving user data.

---

## **General Naming Rules**

### **Variables**

- Use `snake_case` for all variable names.
- Example: `user_name`, `watch_price`

### **Functions**

- Use `snake_case` for function names.
- Example: `get_watch_details`, `create_user_profile`

### **Classes**

- Use `PascalCase` for all class names.
- Example: `UserCreateSchema`, `WatchUpdateParams`

### **Constants**

- Use `UPPERCASE` with underscores for constants.
- Example: `MAX_WATCH_PRICE`, `DEFAULT_USER_ROLE`

---

## **File and Folder Naming**

1. **Files**:

   - Use `snake_case` for file names.
   - Examples: `user_schemas.py`, `watch_services.py`
2. **Folders**:

   - Use lowercase for folder names.
   - Examples: `schemas/`, `services/`

---

## **Additional Notes**

1. **Be Consistent**:

   - Follow these conventions strictly to ensure code readability and maintainability.
   - If unclear, prioritize clarity over brevity.
2. **Resource Abbreviations**:

   - Use one-letter abbreviations for common resources to keep names concise:
     - `W`: Watch
     - `U`: User
     - `C`: Collection
     - `B`: Brand
3. **Document Changes**:

   - Update this guide whenever new conventions are introduced or existing ones are modified.

---

## **Quick Reference Table**


| **Entity** | **Naming Rule**                       | **Example**                      |
| ---------- | ------------------------------------- | -------------------------------- |
| Schemas    | `<Resource><Operation>[Suffix]Schema` | `WCrSchema`, `UReResponseSchema` |
| Models     | Plural names with`Model` suffix       | `WatchesModel`, `UsersModel`     |
| Endpoints  | `/api/<resource>/<version>/<action>/` | `/api/watches/v1/create/`        |
| Variables  | `snake_case`                          | `watch_name`, `user_email`       |
| Functions  | `snake_case`                          | `get_user_profile`               |
| Classes    | `PascalCase`                          | `UserCreateSchema`               |
| Constants  | `UPPERCASE`                           | `MAX_WATCH_PRICE`                |
| Files      | `snake_case`                          | `user_schemas.py`                |
| Folders    | `lowercase`                           | `schemas/`, `services/`          |

---

This guide ensures consistency and readability across the Montana Swiss Watches Website API. By adhering to these conventions, we can create a clean, scalable, and maintainable codebase.

# **Naming Conventions for Montana Swiss Watches Website API**

This document defines the naming conventions to be followed across the Montana Swiss Watches Website API. Consistent naming ensures clarity, maintainability, and efficiency in both individual and team development.

---

## **Naming Keywords**

The following abbreviations are used as keywords to represent CRUD (Create, Read, Update, Delete) operations in resource names:


| **Keyword** | **Operation**     | **Description**                            |
| ----------- | ----------------- | ------------------------------------------ |
| `Cr`        | Create            | Represents creating a new resource.        |
| `Up`        | Update            | Represents updating an existing resource.  |
| `De`        | Delete            | Represents deleting a resource.            |
| `Re`        | Read (Get/Select) | Represents fetching or reading a resource. |

---

## **Schema Naming Guide**

Schemas follow the format:
**`<Resource><Operation>[Suffix]Schema`**

### **Components**

1. **`Resource`**: A short abbreviation representing the entity being acted upon (e.g., `W` for Watch, `U` for User).
2. **`Operation`**: A two-letter abbreviation for the CRUD operation (`Cr`, `Up`, `De`, `Re`).
3. **`Suffix`** *(optional)*: Additional context for the schema:
   - `ParamsSchema`: Used for input parameters.
   - `ResponseSchema`: Used for API responses.
   - `DetailSchema`: Used for detailed or nested object representations.

### **Examples**


| **Resource** | **Operation** | **Suffix**       | **Schema Name**     | **Description**                          |
| ------------ | ------------- | ---------------- | ------------------- | ---------------------------------------- |
| `W`          | `Cr`          | None             | `WCrSchema`         | Schema for creating a watch.             |
| `W`          | `Up`          | `ParamsSchema`   | `WUpParamsSchema`   | Schema for input data to update a watch. |
| `W`          | `Re`          | `ResponseSchema` | `WReResponseSchema` | Schema for watch data in API responses.  |
| `U`          | `Cr`          | None             | `UCrSchema`         | Schema for creating a user.              |
| `U`          | `Re`          | `ResponseSchema` | `UReResponseSchema` | Schema for user data in API responses.   |

---

## **API Endpoint Naming**

- **Format**: Use **kebab-case** for API endpoints.
- **Structure**: `/api/<resource>/<version>/<action>/`
- Examples:
  - `/api/watches/v1/create/` for creating a new watch.
  - `/api/users/v1/get/` for retrieving user data.

---

## **General Naming Rules**

### **Variables**

- Use `snake_case` for all variable names.
- Example: `user_name`, `watch_price`

### **Functions**

- Use `snake_case` for function names.
- Example: `get_watch_details`, `create_user_profile`

### **Classes**

- Use `PascalCase` for all class names.
- Example: `UserCreateSchema`, `WatchUpdateParams`

### **Constants**

- Use `UPPERCASE` with underscores for constants.
- Example: `MAX_WATCH_PRICE`, `DEFAULT_USER_ROLE`

---

## **File and Folder Naming**

1. **Files**:

   - Use `snake_case` for file names.
   - Examples: `user_schemas.py`, `watch_services.py`
2. **Folders**:

   - Use lowercase for folder names.
   - Examples: `schemas/`, `services/`

---

## **Additional Notes**

1. **Be Consistent**:

   - Follow these conventions strictly to ensure code readability and maintainability.
   - If unclear, prioritize clarity over brevity.
2. **Resource Abbreviations**:

   - Use one-letter abbreviations for common resources to keep names concise:
     - `W`: Watch
     - `U`: User
     - `C`: Collection
     - `B`: Brand
3. **Document Changes**:

   - Update this guide whenever new conventions are introduced or existing ones are modified.

---

## **Quick Reference Table**


| **Entity** | **Naming Rule**                       | **Example**                      |
| ---------- | ------------------------------------- | -------------------------------- |
| Schemas    | `<Resource><Operation>[Suffix]Schema` | `WCrSchema`, `UReResponseSchema` |
| Endpoints  | `/api/<resource>/<version>/<action>/` | `/api/watches/v1/create/`        |
| Variables  | `snake_case`                          | `watch_name`, `user_email`       |
| Functions  | `snake_case`                          | `get_user_profile`               |
| Classes    | `PascalCase`                          | `UserCreateSchema`               |
| Constants  | `UPPERCASE`                           | `MAX_WATCH_PRICE`                |
| Files      | `snake_case`                          | `user_schemas.py`                |
| Folders    | `lowercase`                           | `schemas/`, `services/`          |

---

This guide ensures consistency and readability across the Montana Swiss Watches Website API. By adhering to these conventions, we can create a clean, scalable, and maintainable codebase.

naming keywords:

* Cr: Create
* Up: Update
* De: Delete
* Re: Read(Select/Get)
