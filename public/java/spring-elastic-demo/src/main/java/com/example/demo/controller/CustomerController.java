package com.example.demo.controller;

import com.example.demo.jpa.CustomerEntity;
import com.example.demo.jpa.CustomerRepository;
import com.example.demo.jpa.OrderEntity;
import com.example.demo.jpa.OrderRepository;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;

@Controller
public class CustomerController {

    private final CustomerRepository customerRepo;
    private final OrderRepository orderRepo;

    public CustomerController(CustomerRepository customerRepo, OrderRepository orderRepo) {
        this.customerRepo = customerRepo;
        this.orderRepo = orderRepo;
    }

    @GetMapping("/")
    public String index(Model model) {
        // Read directly from PostgreSQL without any sync step
        model.addAttribute("customers", customerRepo.findAll());
        return "index"; // loads templates/index.html
    }

    @GetMapping("/customers")
    public String viewCustomers(Model model) {
        List<CustomerEntity> list = customerRepo.findAll();
        model.addAttribute("customers", list);
        return "customers"; // refers to src/main/resources/templates/customers.html
    }

    @GetMapping("/customers/{id}/orders")
    public String viewCustomerOrders(@PathVariable("id") Long customerNumber, Model model) {
        CustomerEntity customer = customerRepo.findById(customerNumber)
                .orElseThrow(() -> new IllegalArgumentException("Customer not found: " + customerNumber));

        List<OrderEntity> orders = orderRepo.findByCustomerNumberOrderByOrderDateDesc(customerNumber);

        model.addAttribute("customer", customer);
        model.addAttribute("orders", orders);
        return "customer-orders"; // loads src/main/resources/templates/customer-orders.html
    }

    @GetMapping("/customers/{customerNumber}/orders/{orderNumber}/edit")
    public String showEditForm(
            @PathVariable("customerNumber") Long customerId,
            @PathVariable("orderNumber") Integer orderId,
            Model model) {

        CustomerEntity customer = customerRepo.findById(customerId)
                .orElseThrow(() -> new IllegalArgumentException("Invalid customer ID: " + customerId));

        OrderEntity orderEntity = orderRepo.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

        model.addAttribute("customer", customer);
        model.addAttribute("order", orderEntity);
        return "order-form";
    }

    @GetMapping("/customers/{customerNumber}/orders/{orderNumber}/details")
    public String showDetailsForm(
            @PathVariable("customerNumber") Long customerId,
            @PathVariable("orderNumber") Integer orderId,
            Model model) {

        CustomerEntity customer = customerRepo.findById(customerId)
                .orElseThrow(() -> new IllegalArgumentException("Invalid customer ID: " + customerId));

        OrderEntity orderEntity = orderRepo.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

        model.addAttribute("customer", customer);
        model.addAttribute("order", orderEntity);
        return "redirect:/product/search/" + customerId + "/" + orderId;
    }
}