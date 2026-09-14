package com.example.demo.controller;

import com.example.demo.elasticsearch.ProductDocument;
import com.example.demo.elasticsearch.ProductSearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Collections;
import java.util.List;

@Controller
public class ProductSearchController {

    private final ProductSearchService searchService;

    @Autowired
    public ProductSearchController(ProductSearchService searchService) {
        this.searchService = searchService;
    }

    /**
     * Renders the search page for a specific customer/order context.
     * With no query param, shows an empty form. With ?q=..., runs the
     * full-text search and displays results.
     *
     * customerId and orderNumber come from the URL path (e.g. so links to
     * this page - and links out of it, like the "Order" links - can carry
     * that context forward without needing session state).
     */
    @GetMapping("/product/search/{customerId}/{orderNumber}")
    public String search(@PathVariable Integer customerId,
            @PathVariable Integer orderNumber,
            @RequestParam(name = "q", required = false) String q,
            Model model) {
        List<ProductDocument> results = (q != null && !q.isBlank())
                ? searchService.searchByText(q)
                : Collections.emptyList();

        model.addAttribute("customerId", customerId);
        model.addAttribute("orderNumber", orderNumber);
        model.addAttribute("query", q);
        model.addAttribute("results", results);
        model.addAttribute("hasSearched", q != null && !q.isBlank());

        return "products-search"; // resolves to templates/products-search.html
    }
}