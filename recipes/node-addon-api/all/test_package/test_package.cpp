// Example from node-addon-api:
// https://github.com/nodejs/node-addon-api/blob/main/doc/addon.md

#include <napi.h>

class ExampleAddon : public Napi::Addon<ExampleAddon> {
 public:
  ExampleAddon(Napi::Env env, Napi::Object exports) {
    // In the constructor we declare the functions the add-on makes available
    // to JavaScript.
    DefineAddon(exports, {
      InstanceMethod("increment", &ExampleAddon::Increment),
    });
  }
 private:

  // This method has access to the data stored in the environment because it is
  // an instance method of `ExampleAddon` and because it was listed among the
  // property descriptors passed to `DefineAddon()` in the constructor.
  Napi::Value Increment(const Napi::CallbackInfo& info) {
    return Napi::Number::New(info.Env(), ++value);
  }

  // Data stored in these variables is unique to each instance of the add-on.
  uint32_t value = 42;
};

// The macro announces that instances of the class `ExampleAddon` will be
// created for each instance of the add-on that must be loaded into Node.js.
NODE_API_ADDON(ExampleAddon)
