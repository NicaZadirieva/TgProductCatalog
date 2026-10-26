import ProductItemView from "../ProductItemView";
import ProductListProps from "./ProductList.props";
import styles from "./index.module.css";

export default function ProductList({ items }: ProductListProps) {
  return (
    <div className={styles["product_list"]}>
      {items.map((item) => (
        <ProductItemView
          productId={item.id}
          key={item.id}
          name={item.name}
          photoLink={item.photoLink}
        />
      ))}
    </div>
  );
}
