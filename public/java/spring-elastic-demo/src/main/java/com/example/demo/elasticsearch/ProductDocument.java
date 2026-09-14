package com.example.demo.elasticsearch;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;
import org.springframework.data.elasticsearch.annotations.FieldType;
import org.springframework.data.elasticsearch.annotations.InnerField;
import org.springframework.data.elasticsearch.annotations.MultiField;

@Document(indexName = "products")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ProductDocument {

    @Id
    private String productCode;

    // Analyzed for full-text search ("productName"), plus an exact/sortable
    // sub-field ("productName.raw") for filtering or alphabetical sorting.
    @MultiField(mainField = @Field(name = "productname", type = FieldType.Text), otherFields = @InnerField(suffix = "raw", type = FieldType.Keyword))
    private String productName;

    @Field(type = FieldType.Keyword)
    private String productScale;

    @Field(type = FieldType.Keyword)
    private String productVendor;

    @Field(name = "productdescription", type = FieldType.Text)
    private String productDescription;

    @Field(type = FieldType.Integer)
    private Short quantityInStock;

    @Field(name = "buyprice", type = FieldType.Double)
    private Double buyPrice;

    @Field(name = "msrp", type = FieldType.Double)
    private Double msrp;

    @Field(name = "productline", type = FieldType.Keyword)
    private String productLine;

}