import ItemForm from "../components/EntryForm";

function Item() {
  return (
    <ItemForm
      descriptionRoute="api/descriptionsLC/"
      entriesRoute="api/entriesLC/"
    />
  );
}

export default Item;
