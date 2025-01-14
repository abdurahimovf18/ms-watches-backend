"""
This file contains utility functions for creating dynamic SQLAlchemy ORM models and handling
many-to-many relationships, foreign key columns, and table manipulations.

The main function, `create_many_to_many_model`, dynamically generates an intermediary SQLAlchemy
model to represent a many-to-many relationship between two given models. This is useful for 
flexible relationships between entities without needing to manually define intermediary models.

Functions include:
- Handling foreign key column creation.
- Plural-to-singular conversion for table names.
- Index generation for performance optimization.
- Cloning columns from existing tables.
"""


from typing import Callable, Any, Sequence
from sqlalchemy import Column, ForeignKey, Index, Table
from sqlalchemy.exc import DuplicateColumnError
from sqlalchemy.orm import relationship
from dataclasses import dataclass, field
from loguru import logger

from .base_model import BaseModel
from src.core.base_settings import DB_ID_TYPE


@dataclass
class ModelArgs:
    """
    Represents the configuration arguments for a model in relation to its many-to-many relationship.
    
    Attributes:
        model (BaseModel | Table): The SQLAlchemy ORM model or Table instance.
        foreign_key_type (Any): The type for foreign key columns. Defaults to `DB_ID_TYPE`.
        include_index (bool): Whether to include indexes on foreign key columns. Defaults to True.
        on_delete (str): The action to take on delete (e.g., "SET NULL"). Defaults to "SET NULL".
        nullable (bool): Whether the foreign key column should be nullable. Defaults to True.
        unique (bool): Whether the foreign key column should be unique. Defaults to False.
        relate_as_singular (bool): Whether to treat the related table as singular. Defaults to False.
        tablename (str | None): Custom tablename for the many-to-many relationship. Defaults to None.
    """
    model: BaseModel | Table
    foreign_key_type: Any = field(default=DB_ID_TYPE)
    include_index: bool = field(default=False)
    on_delete: str = field(default="SET NULL")
    nullable: bool = field(default=True)
    unique: bool = field(default=False)
    relate_as_singular: bool = field(default=False)
    tablename: str | None = field(default=None)
    back_populates: str | None = field(default=None)


@dataclass
class RelationshipArgs:
    """
    Represents the configuration arguments for defining the relationship between models in a many-to-many relationship.

    This class encapsulates parameters that control the relationship's behavior, such as the relationship name and
    whether to return the ORM model or not.

    Attributes:
        relation_name (str | None): The name of the relationship. This is used to establish the name of the
                                     relationship between models, particularly for `back_populates` or other
                                     relationship configuration purposes.
        return_orm (bool): Whether to return the generated ORM model (True) or the intermediary table (False).
                           Defaults to True, indicating that the ORM model should be returned.

    Example:
        relationship_args = RelationshipArgs(
            relation_name="model_a_model_b",
            return_orm=True
        )
    """
    
    relation_name: str | None = field(default=None)
    return_orm: bool = field(default=True)



class ModelManager:
    """
    Manages the dynamic generation of many-to-many relationship models, columns, and indexes.
    This includes generating foreign key columns, table names, and index configurations for
    intermediary tables.

    Attributes:
        args (ModelArgs): The configuration arguments for the model.
        model (BaseModel): The SQLAlchemy ORM model.
        all_args (Sequence[ModelArgs]): A sequence of `ModelArgs` for all related models.
    """

    def __init__(self, args: ModelArgs, all_args: Sequence[ModelArgs], relation_args: RelationshipArgs):
        """
        Initializes the ModelManager with configuration arguments and models for the many-to-many relationship.

        Args:
            args (ModelArgs): The configuration for a single model.
            all_args (Sequence[ModelArgs]): The sequence of all related models.
        """

        self.relation_args = relation_args
        self.args = args
        self.model = self.cast_to_orm(self.args.model)
        self.all_args = all_args

    @property
    def relationship(self) -> list[Any]:
        """
        Retrieves the relationship definition for the current model.

        This property defines the relationship between models using SQLAlchemy's 
        `relationship()` function. It checks whether the `back_populates` attribute 
        is provided in the `ModelArgs`. If `back_populates` is defined, it creates a 
        `relationship()` linking the current model to the related model.

        Returns:
            list[Any]: A list containing the relationship(s) for the model. 
            If no `back_populates` is defined, an empty list is returned. 
            The list will contain a `relationship()` object if a relationship is defined.
        """
        if self.args.back_populates is None:
            return []
        
        return [
            relationship(self.model, 
                        back_populates=self.args.back_populates)
        ]


    @staticmethod
    def _is_table(value: Any) -> bool:
        """
        Checks whether a value is an instance of SQLAlchemy's `Table`.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is a `Table` instance, False otherwise.
        """

        return isinstance(value, Table)
    
    @staticmethod
    def _is_model(value: Any) -> bool:
        """
        Checks whether a value is an SQLAlchemy ORM model.

        Args:
            value (Any): The value to check.

        Returns:
            bool: True if the value is an ORM model, False otherwise.
        """

        return hasattr(value, "__table__")
    
    def clone_columns(self, value: BaseModel | Table) -> list[Column]:
        """
        Clones columns from the given SQLAlchemy model or table.

        Args:
            value (BaseModel | Table): The model or table whose columns to clone.

        Returns:
            list[Column]: A list of cloned columns.
        
        Raises:
            TypeError: If the value is neither a model nor a table.
        """

        if self._is_model(value):
            table = value.__table__
        elif self._is_table(value):
            table = value
        else:
            raise TypeError("Input must be a SQLAlchemy ORM model or a Table instance.")
        
        return [col.copy() for col in table.columns.values()]
    
    def cast_to_orm(self, value: Table | BaseModel) -> BaseModel:
        """
        Converts a SQLAlchemy `Table` instance to an ORM model.

        Args:
            value (Table | BaseModel): The value to convert.

        Returns:
            BaseModel: The corresponding ORM model.
        
        Raises:
            TypeError: If the value is neither a model nor a table.
        """

        if self._is_model(value):
            return value
        if self._is_table(value):
            return self.to_orm(table=value)
        
        raise TypeError("Input must be a SQLAlchemy ORM model or a Table instance.")

    def to_orm(self, table: Table) -> BaseModel:
        """
        Creates an ORM model from a given `Table` instance.

        Args:
            table (Table): The table to convert into an ORM model.

        Returns:
            BaseModel: The ORM model.
        """

        class TempOrmModel(BaseModel):
            __table__ = table

        return TempOrmModel

    @property
    def col_tablename(self) -> str:
        """
        Returns the table name for the foreign key column, considering custom names or plural-to-singular conversions.

        Returns:
            str: The table name for the foreign key column.
        """

        if self.args.tablename is not None:
            return self.args.tablename
        
        if self.args.relate_as_singular:
            return self.plural_to_one(self.tablename)
        
        return self.tablename
    
    @staticmethod
    def plural_to_one(value: str) -> str:
        """
        Converts a plural table name to a singular one.

        Args:
            value (str): The plural table name.

        Returns:
            str: The singular version of the table name.
        """

        if value.endswith("ies"):
            return value[:-3] + "y"
        if value.endswith("es") and value[-3:-2] in ("ch", "sh", "x", "z"):
            return value[:-2]
        if value.endswith("s"):
            return value[:-1]
        return value
    
    @property
    def tablename(self) -> str:
        """
        Returns the table name for the model.

        Returns:
            str: The table name.
        """

        return self.get_table_name(self.args)
    
    @staticmethod
    def get_table_name(args: ModelArgs) -> str:
        """
        Gets the table name for a model from the `ModelArgs`.

        Args:
            args (ModelArgs): The configuration for the model.

        Returns:
            str: The table name of the model.
        """

        return args.model.__tablename__
    
    @property
    def model_name(self) -> str:
        """
        Returns the name of the model.

        Returns:
            str: The model name.
        """

        return self.model.__name__
    
    @property
    def relation_name(self) -> str:
        """
        Generates the relation name by joining the table names of all related models.

        Returns:
            str: The relation name.
        """

        if self.relation_args is not None:
            return self.relation_args.relation_name
        
        return "_to_".join(map(self.get_table_name, self.all_args))
    
    @property
    def relation_table_name(self) -> str:
        """
        Generates the relation table name by joining the table names of all related models.

        Returns:
            str: The relation table name.
        """

        return "_to_".join(map(self.get_table_name, self.all_args))
    
    @property
    def column_name(self):
        """
        Generates the name for the foreign key column.

        Returns:
            str: The foreign key column name.
        """

        return f"{self.col_tablename}_id"
    
    @property
    def fk_table_pk(self) -> str:
        """
        Returns the primary key column of the related table.

        Returns:
            str: The foreign key table primary key.
        """

        return f"{self.tablename}.id"
    
    @property
    def on_delete(self) -> str:
        """
        Returns the configured `on_delete` action for the foreign key.

        Returns:
            str: The `on_delete` action.
        """

        return self.args.on_delete
    
    @property
    def nullable(self) -> bool:
        """
        Returns whether the foreign key column should be nullable.

        Returns:
            bool: True if nullable, False otherwise.
        """

        return self.args.nullable

    @property
    def indexes(self) -> list[Index]:
        """
        Returns the list of indexes for the foreign key column.

        Returns:
            list[Index]: A list of SQLAlchemy `Index` objects.
        """

        return [
            Index(f"{self.relation_name}_index_{self.column_name}", self.column_name),
        ]
    
    @property
    def fk_column(self) -> Column:
        """
        Generates the foreign key column for the many-to-many relationship.

        Returns:
            Column: The SQLAlchemy `Column` object representing the foreign key.
        """

        return Column(
            self.column_name,
            DB_ID_TYPE,
            ForeignKey(self.fk_table_pk, ondelete=self.on_delete),
            nullable=self.nullable
        )
    
    @property
    def columns(self) -> list[Column]:
        """
        Returns a list of columns for the intermediary model, including the foreign key column.

        Returns:
            list[Column]: A list of columns for the intermediary table.
        """

        return [
            self.fk_column,
        ]
    
    def manager_closure(all_args, relation_args) -> Callable:
        """
        Returns a closure function for creating `ModelManager` instances with the provided arguments.

        Args:
            all_args (Sequence[ModelArgs]): A sequence of `ModelArgs` for all related models.

        Returns:
            Callable: A closure function that returns `ModelManager` instances.
        """

        def closure(args: ModelArgs) -> ModelManager:
            return ModelManager(all_args=all_args, args=args, relation_args=relation_args)
        return closure
    
    @property
    def default_columns(self) -> list[Column]:
        """
        Returns the default columns for an empty intermediary model.

        Returns:
            list[Column]: The default columns.
        """

        class TempOrmModel(BaseModel):
            pass

        return self.clone_columns(TempOrmModel)
    

class ModelManagerHandler:
    """
    Handles the creation and management of multiple `ModelManager` instances for many-to-many
    relationships. It consolidates columns and indexes across multiple models for efficient
    table and model generation.
    """

    def __init__(self, *args: ModelManager, relation_args: RelationshipArgs):
        """
        Initializes the `ModelManagerHandler` with the provided `ModelManager` instances.

        Args:
            args (ModelManager): The manager instances to handle.
            relation_args (RelationshipArgs): The args that will handle overall relationship
        """
        
        self.relation_args = relation_args
        self.args = args
        self.managers = self.get_managers()
        self._first = self.managers[0]

    def get_columns(self) -> list[Column]:
        """
        Returns the combined list of columns from all the managers.

        Returns:
            list[Column]: The list of columns from all managers.
        """

        columns = []
        for manager in self.managers:
            columns.extend(manager.columns)

        columns.extend(self.managers[0].default_columns)

        return columns

    def get_indexes(self) -> list[Column]:
        """
        Returns the combined list of indexes from all the managers.

        Returns:
            list[Column]: The list of indexes from all managers.
        """

        indexes = []
        for manager in self.managers:
            indexes.extend(manager.indexes)

        return indexes
    
    def get_relationships(self) -> list[Any]:
        """
        Retrieves the relationships for the models managed by the current instance.

        This method iterates over all the `ModelManager` instances stored in `self.managers`, 
        and for each one, it collects the `relationship` attribute (if defined) into a list. 
        The `relationship` attribute is typically used to define the relationships between 
        tables in SQLAlchemy models.

        Returns:
            list[Any]: A list of relationships defined in the managed models. This can include 
            SQLAlchemy `relationship()` instances or other types of relationship data.
        """
        relationships = []
        for manager in self.managers:
            relationships.extend(manager.relationship)

        return relationships

    def get_managers(self) -> tuple[ModelManager]:
        """
        Creates `ModelManager` instances from the provided arguments.

        Args:
            args (tuple[ModelArgs]): The arguments for each manager.

        Returns:
            tuple[ModelManager]: The created manager instances.
        """

        manager_closure = ModelManager.manager_closure(all_args=self.args, relation_args=self.relation_args)
        managers: tuple[ModelManager] = tuple(map(
            manager_closure, self.args
        ))

        return managers
    
    @property
    def _is_duplicated_tablenames(self) -> bool:
        """
        Checks if there are duplicate table names across all managers.

        Returns:
            bool: True if there are duplicate table names, False otherwise.
        """

        tablenames: set[str] = set()
        
        for manager in self.managers:
            if manager.col_tablename in tablenames:
                return True
            tablenames.add(manager.col_tablename)

        return False

    def generate_table(self) -> Table:
        """
        Generates the intermediary table by combining the columns and indexes from all managers.

        Returns:
            Table: The generated SQLAlchemy `Table` object.
        
        Raises:
            ValueError: If there are duplicate table names across the managers.
        """

        columns: list[Column] = self.get_columns()
        indexes: list[Index] = self.get_indexes()

        try:
            table = Table(
                self.relation_name,
                BaseModel.metadata,
                *columns,
                *indexes,
            )
        except DuplicateColumnError:
            if self._is_duplicated_tablenames:
                raise ValueError("Models should have diffrent table names, "
                                 "if you want to relate one model to itself please add \"tablename\" parameter "
                                 "on the ModelArgs")
        return table
    
    @property
    def relation_name(self) -> str:
        """
        Returns the relation name for the many-to-many relationship by joining the table names of all related models.

        Returns:
            str: The relation name, typically used for naming the intermediary table in a many-to-many relationship.
        """
        return self._first.relation_name
    
    @property
    def model_name(self) -> str:
        """
        Generates the model name for the many-to-many relationship. The name is formed by concatenating 
        the model names of all related models, removing the "Model" suffix, and joining them with "To".

        Returns:
            str: The generated model name in the form "Model1ToModel2", without the "Model" suffix.
        """
        return "To".join(manager.model_name.removesuffix("Model") for manager in self.managers)
    
    def generate_orm(self) -> BaseModel:
        """
        Generates a new SQLAlchemy ORM model based on the intermediary table created for the many-to-many relationship.

        This method uses the `generate_table` method to generate the table and then creates a dynamic ORM class 
        by attaching the generated table to the new model. The model class name is derived from the related models' names.

        Returns:
            BaseModel: The dynamically created SQLAlchemy ORM model class representing the many-to-many relationship.
        """
        

        table = self.generate_table()

        class M2M(BaseModel):
            __table__ = table
            __allow_unmapped__ = True

        M2M.__name__ = self.model_name
        self.set_relations(model=M2M)

        return M2M
    
    def set_relations(self, model: BaseModel) -> None:
        """
        Dynamically sets the relationships on the given model class.

        This method iterates through the managers, retrieves the relationship objects
        and assigns them to the model class using dynamic attribute names based on the 
        `back_populates` attribute from the `ModelArgs` of each manager.

        Args:
            model (BaseModel): The SQLAlchemy model to which the relationships will be 
                                dynamically added. The relationships are added as 
                                attributes on this model.
        
        Returns:
            None: This method modifies the passed `model` in-place by dynamically adding 
                relationships as attributes.
        
        Example:
            If you have a model like `User` and you want to dynamically set its 
            relationships, you would call `set_relations` like this:
            
            set_relations(User)

            The relationships will be added dynamically to the `User` model.
        """
        relationships: list[Any] = self.get_relationships()

        # Generate dynamic relationship names based on back_populates for each manager
        name_gen = (manager.col_tablename for manager in self.managers if manager.args.back_populates is not None)

        # Dynamically set each relationship on the model using the generated names
        [setattr(model, name, relation) for name, relation in zip(name_gen, relationships)]

    def generate_m2m(self) -> BaseModel:
        """
        Generates m2m relationship according to params
        """

        if self.relation_args.return_orm:
            return self.generate_orm()
        
        return self.generate_table()
    

def create_m2m(arg1: ModelArgs, arg2: ModelArgs, relation_args: RelationshipArgs) -> BaseModel:
    """
    Creates an intermediary many-to-many model or table based on the provided `ModelArgs` and `RelationshipArgs`.

    This function takes two `ModelArgs` configurations and a `RelationshipArgs` configuration to dynamically generate
    either a SQLAlchemy ORM model representing a many-to-many relationship or an intermediary table that links
    two models. It initializes a `ModelManagerHandler` and uses it to generate the desired model or table.

    Args:
        arg1 (ModelArgs): The configuration for the first model in the many-to-many relationship, including details 
                          such as foreign key, nullable, and other attributes.
        arg2 (ModelArgs): The configuration for the second model in the many-to-many relationship, similar to `arg1`.
        relation_args (RelationshipArgs): Additional relationship-specific arguments, such as `back_populates` or 
                                          `cascade`, to configure how the two models are related.

    Returns:
        BaseModel: A dynamically generated SQLAlchemy ORM model if the relationship is established via ORM. 
                   This model represents the many-to-many relationship. If `return_orm` is False, the function 
                   will return the intermediary `Table` object instead.
    
    Example:
        To create a many-to-many relationship between `ModelA` and `ModelB`, you can call the function like this:

        create_m2m(
            ModelArgs(model=ModelA, ...),
            ModelArgs(model=ModelB, ...),
            RelationshipArgs(...)
        )

        This will create an intermediary model/table with the necessary relationships and configurations.
    """
    manager_handler = ModelManagerHandler(arg1, arg2, relation_args=relation_args)

    m2m = manager_handler.generate_m2m()
    
    return m2m
