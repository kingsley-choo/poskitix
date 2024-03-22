package com.poskitix.cs102.user;

// import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@CrossOrigin
@RequestMapping("/user")
public class UserController {
    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    @GetMapping("/{uid}")
    public User getUserById(@PathVariable int uid) {
        return service.getUserById(uid);
    }

    @GetMapping
    public Map<Integer, User> getUsersByMultipleIds(@RequestParam("uid") List<Integer> uids) {
        return service.getUsersByIds(uids).stream().collect(Collectors.toMap(User::getUid, user -> user));
    }

    @GetMapping
    public Map<Integer, User> getAllUsers() {
        return service.getAllUsers().stream().collect(Collectors.toMap(User::getUid, user -> user));
    }

    // @PostMapping("/create")
    // public User create(@RequestBody User user) {
    // return service.saveUser(user);
    // }
    //
    // @DeleteMapping
    // public void delete(@RequestParam int id) {
    // service.deleteUserById(id);
    // }
}
