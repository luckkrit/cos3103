package com.example.demo.controller;

import com.example.demo.jpa.CustomerEntity;
import com.example.demo.jpa.CustomerRepository;
import com.example.demo.jpa.OrderEntity;
import com.example.demo.jpa.OrderRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;

@Controller
@RequestMapping("/orders")
public class OrderViewController {

    private final OrderRepository orderRepo;
    private final CustomerRepository customerRepo;

    public OrderViewController(OrderRepository orderRepo, CustomerRepository customerRepo) {
        this.orderRepo = orderRepo;
        this.customerRepo = customerRepo;
    }

    // 1. Display the creation form
    @GetMapping("/new")
    public String showCreateForm(@RequestParam("customerId") Long customerId, Model model) {
        CustomerEntity customer = customerRepo.findById(customerId)
                .orElseThrow(() -> new IllegalArgumentException("Invalid customer ID: " + customerId));

        OrderEntity newOrder = new OrderEntity();
        newOrder.setCustomerNumber(customerId);
        newOrder.setOrderDate(LocalDateTime.now());
        newOrder.setStatus("In Process");

        model.addAttribute("customer", customer);
        model.addAttribute("order", newOrder);
        return "order-form"; // loads templates/order-form.html
    }

    // 2. Process form submission
    @PostMapping("/save")
    public String saveOrder(@ModelAttribute("order") OrderEntity order) {
        // If orderNumber isn't auto-generated, assign the next available number:
        if (order.getOrderNumber() == null) {
            int maxId = orderRepo.findAll().stream()
                    .mapToInt(OrderEntity::getOrderNumber)
                    .max()
                    .orElse(10000);
            order.setOrderNumber(maxId + 1);
        } else {
            // --- EDIT EXISTING ORDER LOGIC ---
            // Optional: Ensure original creation date is preserved if not present in form
            OrderEntity existing = orderRepo.findById(order.getOrderNumber()).orElse(null);
            if (existing != null && order.getOrderDate() == null) {
                order.setOrderDate(existing.getOrderDate());
            }
        }

        orderRepo.save(order);

        // Redirect back to the customer's order list
        return "redirect:/customers/" + order.getCustomerNumber() + "/orders";
    }

}